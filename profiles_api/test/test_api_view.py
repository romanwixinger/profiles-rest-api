from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_api import permissions

from profiles_api.test.test_serializer import TestSerializer, TestDeserializer
from profiles_api.test.test_model import Test
from profiles_api.test.test_service import TestService


class TestViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating tests"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = TestSerializer
    queryset = Test.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)


class TestView(APIView):
    """Handles creating and reading tests"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def get(self, request):
        """Retrieves selected tests"""

        query_params_dict = self.request.query_params.dict()
        tests = TestService.get_tests(query_params_dict)

        if tests.count() == 0:
            return Response(status=204)

        serializer = TestSerializer(tests, many=True)
        return Response(data=serializer.data, status=200)

    def post(self, request):
        """Create new test"""

        deserializer = TestDeserializer(data=request.data)

        if deserializer.is_valid():

            user = self.request.user
            validated_data = deserializer.validated_data
            validated_data['user_id'] = user.id
            try:
                test = deserializer.create(validated_data)
            except LookupError:
                return Response(
                    deserializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            if test is None:
                return Response(
                    deserializer.errors,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            serializer = TestSerializer(test)
            return Response(data=serializer.data, status=201)

        return Response(
            deserializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class RecommendedTestView(APIView):
    """Recommends tests bases on results of completed tests"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def get(self, request):
        """Retrieves recommended tests"""

        start = self.request.query_params.get('start', None)
        number = self.request.query_params.get('number', None)

        nr = int(number) if number is not None else 1
        nr += int(start) if start is not None else 0

        tests_id = TestService.get_recommended_tests(request.user, number=nr)
        tests = Test.objects.filter(id__in=tests_id) if tests_id != [] else None
        if tests is None:
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

        if start is not None:
            tests = tests[min(abs(int(start)), tests.count()):]
        if number is not None:
            tests = tests[:max(0, min(int(number), tests.count()))]

        if tests.count() == 0:
            return Response(status=204)

        serializer = TestSerializer(tests, many=True)
        return Response(data=serializer.data, status=200)

