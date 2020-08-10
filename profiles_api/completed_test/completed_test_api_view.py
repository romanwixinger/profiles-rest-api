from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_api import permissions

from profiles_api.completed_test.completed_test_serializer import CompletedTestSerializer, CompletedTestDeserializer
from profiles_api.completed_test.completed_test_serializer import CompletedTestPatchDeserializer
from profiles_api.completed_test.completed_test_model import CompletedTest
from profiles_api.completed_test.completed_test_service import CompletedTestService


class CompletedTestViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating completed tests"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = CompletedTestSerializer
    queryset = CompletedTest.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)


class CompletedTestView(APIView):
    """Handles getting and creating completed tests"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def get(self, request, **kwargs):
        """Get a completed test"""

        query_params_dict = self.request.query_params.dict()

        pk = self.kwargs.get('pk')
        if pk is not None:
            query_params_dict['id'] = pk

        if 'user_id' in query_params_dict:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if not self.request.user.is_superuser:
            print("Here")
            query_params_dict['user_id'] = self.request.user.id
        try:
            completed_tests = CompletedTestService.search_completed_tests(query_params_dict)
        except LookupError:
            return Response(
                {"id": "The completed test with this id does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        except PermissionError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if len(completed_tests) == 0:
            return Response(status=204)

        if pk is None:
            serializer = CompletedTestSerializer(completed_tests, many=True)
        else:
            serializer = CompletedTestSerializer(completed_tests[0], many=False)
        return Response(data=serializer.data, status=200)

    def post(self, request):
        """Create a completed test"""

        deserializer = CompletedTestDeserializer(data=request.data)

        if deserializer.is_valid():

            user = self.request.user
            validated_data = deserializer.validated_data
            validated_data['user_id'] = user.id

            try:
                completed_test = deserializer.create(validated_data)
            except ValueError:
                return Response(
                    {"answers": "The question to one of the answers does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if completed_test is None:
                return Response(
                    deserializer.errors,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            CompletedTestService.get_recommended_subtopics(completed_test)
            completed_test.save()

            serializer = CompletedTestSerializer(completed_test)
            return Response(data=serializer.data, status=201)

        return Response(
            deserializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, *args, **kwargs):
        """Handle a partial update of a completed test and adding answers"""

        pk = self.kwargs.get('pk')

        deserializer = CompletedTestPatchDeserializer(data=request.data)
        if not deserializer.is_valid():
            return Response(
                deserializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = deserializer.validated_data
        validated_data['user_id'] = self.request.user.id

        completed_test = CompletedTestService.get_completed_tests([pk])
        if len(completed_test) == 0:
            return Response(
                {'id': 'The completed test with this id does not exist or does not belong to this user.'},
                status=status.HTTP_404_NOT_FOUND
            )

        completed_test = deserializer.update(instance=completed_test[0],
                                             validated_data=deserializer.validated_data)
        completed_test.save()

        return Response(status=200)

