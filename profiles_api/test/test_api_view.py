from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_api import permissions

from profiles_api.test.test_serializer import TestSerializer
from profiles_api.test.test_model import Test


class TestViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating tests"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = TestSerializer
    queryset = Test.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)


