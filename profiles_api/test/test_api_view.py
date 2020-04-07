from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_api import permissions

from profiles_api.test.test_serializer import TestSerializer, TestDeserializer
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


class TestView(APIView)
    """Handles creating and reading tests"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def get(self, request):
        """Retrieves selected tests"""

        filter_dict = {}
        if 'topic_id' in request.data and request.data['topic_id'].isdigit():
            filter_dict['id'] = int(request.data['topic_id'])
        if 'title' in request.data:
            filter_dict['title'] = request.data['title']

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
