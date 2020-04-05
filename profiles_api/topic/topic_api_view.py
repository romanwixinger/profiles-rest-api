from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

from profiles_api.topic.topic_serializer import TopicSerializer
from profiles_api.topic.topic_model import Topic


class TopicViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating topics"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)


class TopicView(APIView):
    """Custom view for topics"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def get(self, request):
        """Retrieve only certain topics"""
        start = self.request.query_params.get('start', None)
        number = self.request.query_params.get('number', None)

        topics = Topic.objects.all()

        if start is not None:
            topics = topics[min(abs(int(start)), topics.count()):]

        if number is not None:
            topics = topics[:max(0, min(int(number), topics.count()))]

        if topics.count() > 0:
            serializer = TopicSerializer(topics, many=True)
            return Response(data=serializer.data, status=200)
        else:
            return Response(status=204)

    def post(self, request):
        """Create a new topic"""
        topic_name = request.data['topic']
        if topic_name is None or topic_name == '':
            return Response(data='Topic not defined', status=400)

        user = self.request.user

        if user is None or user.id == '':
            return Response(data='User not defined', status=400)
        else:
            topic = Topic.objects.get_or_create(
                name=topic_name,
                user_profile_id=user.id
            )[0]

        serializer = TopicSerializer(topic)
        return Response(data=serializer.data, status=201)
