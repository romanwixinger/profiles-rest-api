from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_api import permissions

from profiles_api.topic.topic_serializer import TopicSerializer, TopicDeserializer
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
    serializer_class = TopicSerializer
    deserializer_class = TopicDeserializer

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

        deserializer = self.deserializer_class(data=request.data)

        if deserializer.is_valid():
            user = self.request.user
            topic_name = request.data['name']
            topic = Topic.objects.get_or_create(
                name=topic_name,
                user_profile_id=user.id
            )[0]

            serializer = TopicSerializer(topic)
            return Response(data=serializer.data, status=201)

        return Response(
            deserializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


