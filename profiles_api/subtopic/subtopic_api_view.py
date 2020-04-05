from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_api import permissions

from profiles_api.subtopic.subtopic_serializer import SubTopicSerializer
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.topic.topic_model import Topic


class SubtopicViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating subtopics"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = SubTopicSerializer
    queryset = Subtopic.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)

    def get_queryset(self):
        """Retrieve only subtopic with certain topic"""
        topic = self.request.query_params.get('topic', None)
        topic_id = self.request.query_params.get('topic_id', None)
        start = self.request.query_params.get('start', None)
        number = self.request.query_params.get('number', None)

        """Return subtopics"""
        if topic is not None:
            filter_dict = {'topic__name': topic}
            subtopics = Subtopic.objects.filter(**filter_dict)
        elif topic_id is not None:
            filter_dict = {'topic__id': topic_id}
            subtopics = Subtopic.objects.filter(**filter_dict)
        else:
            subtopics = Subtopic.objects.all()

        if start is not None:
            subtopics = subtopics[min(abs(int(start)), subtopics.count()):]

        if number is not None:
            subtopics = subtopics[:max(0, min(int(number), subtopics.count()))]

        return subtopics



class CustomSubtopicView(APIView):
    """Custom view for Subtopic"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def get(self, request):
        """Retrieve only certain subtopics"""
        topic = self.request.query_params.get('topic', None)
        topic_id = self.request.query_params.get('topic_id', None)
        start = self.request.query_params.get('start', None)
        number = self.request.query_params.get('number', None)

        if topic is not None:
            filter_dict = {'topic__name': topic}
            subtopics = Subtopic.objects.filter(**filter_dict)
        elif topic_id is not None:
            filter_dict = {'topic__id': topic_id}
            subtopics = Subtopic.objects.filter(**filter_dict)
        else:
            subtopics = Subtopic.objects.all()

        if start is not None:
            subtopics = subtopics[min(abs(int(start)), subtopics.count()):]

        if number is not None:
            subtopics = subtopics[:max(0, min(int(number), subtopics.count()))]

        if subtopics.count() > 0:
            serializer = SubTopicSerializer(subtopics, many=True)
            return Response(data=serializer.data, status=200)
        else:
            return Response(status=204)

    def post(self, request):
        """Create a new subtopic. Additionally a new topic is created if necessary"""
        topic_name = request.data['topic']
        if topic_name is None or topic_name == '':
            return Response(data='Topic not defined', status=400)

        user = self.request.user

        if user is None or user.id == '':
            return Response(data='User not defined', status=400)

        topic = Topic.objects.get_or_create(
            name=topic_name,
            user_profile_id=user.id
        )[0]

        subtopic = Subtopic.objects.get_or_create(
            topic=topic,
            name=request.data['name'],
            html=request.data['html'],
            user_profile_id=user.id
        )[0]

        serializer = SubTopicSerializer(subtopic)

        return Response(data=serializer.data, status=201)
