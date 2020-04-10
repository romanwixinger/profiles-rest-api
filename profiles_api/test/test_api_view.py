from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_api import permissions

from profiles_api.test.test_serializer import TestSerializer, TestDeserializer
from profiles_api.test.test_model import Test
from profiles_api.test.test_service import get_recommended_tests


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

        test_id = self.request.query_params.get('id', None)
        title = self.request.query_params.get('title', None)

        filter_dict = {}
        if test_id is not None and test_id.isdigit():
            print("true")
            filter_dict['id'] = int(test_id)
        if title is not None:
            filter_dict['title'] = title

        tests = Test.objects.filter(**filter_dict)

        start = self.request.query_params.get('start', None)
        number = self.request.query_params.get('number', None)

        if start is not None:
            tests = tests[min(abs(int(start)), tests.count()):]
        if number is not None:
            tests = tests[:max(0, min(int(number), tests.count()))]

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
            test = deserializer.create(validated_data)

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

        tests_id = get_recommended_tests(request.user)
        tests = Test.objects.filter(id__in=tests_id)
        if tests is None:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        start = self.request.query_params.get('start', None)
        number = self.request.query_params.get('number', None)

        if start is not None:
            tests = tests[min(abs(int(start)), tests.count()):]
        if number is not None:
            tests = tests[:max(0, min(int(number), tests.count()))]

        if tests.count() == 0:
            return Response(status=204)

        serializer = TestSerializer(tests, many=True)
        return Response(data=serializer.data, status=200)

