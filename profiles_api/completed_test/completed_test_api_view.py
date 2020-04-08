from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_api import permissions

from profiles_api.completed_test.completed_test_serializer import CompletedTestSerializer
from profiles_api.completed_test.completed_test_model import CompletedTest


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

    def get(self, request):
        """Get a completed test"""

        filter_dict = {}
        completed_test_id = self.request.query_params.get('id', None)

        if completed_test_id is not None:
            filter_dict['id'] = completed_test_id

        completed_test = CompletedTest.objects.filter(**filter_dict)[0] \
            if CompletedTest.objects.filter(**filter_dict).count() > 0 else None
        if completed_test is not None:
            serializer = CompletedTestSerializer(completed_test)
            return Response(data=serializer.data, status=201)

        return Response(status=204)


