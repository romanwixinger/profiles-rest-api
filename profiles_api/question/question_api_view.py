from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_api import permissions

from profiles_api.question.question_serializer import QuestionSerializer, QuestionDeserializer
from profiles_api.question.question_model import Question


class QuestionViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating question items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)

    def get_queryset(self):
        """Retrieve only selected questions depending on query parameters"""
        user_id = self.request.query_params.get('user_id', None)
        topic = self.request.query_params.get('topic', None)
        subtopic = self.request.query_params.get('subtopic', None)
        start = self.request.query_params.get('start', None)
        number = self.request.query_params.get('number', None)

        filter_dict = dict()
        if user_id is not None:
            filter_dict['user_profile__id'] = user_id
        if topic is not None:
            filter_dict['topic'] = topic
        if subtopic is not None:
            filter_dict['subtopic'] = subtopic
        questions = Question.objects.filter(**filter_dict)

        if start is not None:
            questions = questions[min(abs(int(start)), questions.count()):]
        if number is not None:
            questions = questions[:max(0, min(int(number), questions.count()))]

        return questions


class QuestionView(APIView):
    """Custom view for Question"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def get(self, request):
        """Retrieve only certain questions"""
        topic = self.request.query_params.get('topic', None)
        topic_id = self.request.query_params.get('topic_id', None)
        subtopic = self.request.query_params.get('subtopic', None)
        subtopic_id = self.request.query_params.get('subtopic_id', None)
        start = self.request.query_params.get('start', None)
        number = self.request.query_params.get('number', None)

        filter_dict = {}
        if topic is not None:
            filter_dict['topic__name'] = topic
        if topic_id is not None:
            filter_dict['topic__id'] = topic_id
        if subtopic is not None:
            filter_dict['subtopic__name'] = subtopic
        if subtopic_id is not None:
            filter_dict['subtopic__id'] = subtopic_id
        questions = Question.objects.filter(**filter_dict)

        if start is not None:
            questions = questions[min(abs(int(start)), questions.count()):]
        if number is not None:
            questions = questions[:max(0, min(int(number), questions.count()))]

        serializer = QuestionSerializer(questions, many=True)
        return Response(data=serializer.data, status=200)

    def post(self, request):
        """Create a new question. Additionally a new topic and subtopic is created if necessary"""

        user = self.request.user

        if user is None or user.id == '':
            return Response(data='User not defined', status=400)

        deserializer = QuestionDeserializer(data=request.data)

        if deserializer.is_valid():
            deserializer.validated_data['user_id'] = user.id
            question = deserializer.create(deserializer.validated_data)
            question.save()

            serializer = QuestionSerializer(question)
            return Response(data=serializer.data, status=201)

        return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)
