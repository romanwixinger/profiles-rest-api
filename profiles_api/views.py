from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

from profiles_api.topic.topic_model import Topic
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.question.question_model import Question


class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over you application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""
        a_viewset = [
            'Uses actions (list, create,retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)


class AnswerViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating answers"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.AnswerSerializer
    queryset = models.Answer.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)


class TestViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating tests"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.TestSerializer
    queryset = models.Test.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)


class CompletedTestViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating completed tests"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.CompletedTestSerializer
    queryset = models.CompletedTest.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)


class TheoryPageViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating theory pages"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.TheoryPageSerializer
    queryset = models.TheoryPage.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)


class AnswerView(APIView):
    """Custom view for answers"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def get(self, request):
        """Get certain answers of the user"""
        start = self.request.query_params.get('start', None)
        number = self.request.query_params.get('number', None)
        question_id = self.request.query_params.get('question_id', None)
        topic_id = self.request.query_params.get('topic_id', None)
        subtopic_id = self.request.query_params.get('subtopic_id', None)
        user_id = self.request.user.id

        if user_id is None or user_id == '':
            return Response(data='User not defined', status=400)

        filter_dict = dict()
        if question_id is not None and question_id != '':
            filter_dict['question__id'] = question_id
        if topic_id is not None and question_id != '':
            filter_dict['question__topic'] = topic_id
        if subtopic_id is not None and question_id != '':
            filter_dict['question__subtopic'] = subtopic_id
        answers = models.Answer.objects.filter(**filter_dict)

        if start is not None:
            answers =answers[min(abs(int(start)), answers.count()):]
        if number is not None:
            answers = answers[:max(0, min(int(number), answers.count()))]

        if answers.count() > 0:
            serializer = serializers.AnswerSerializer(answers, many=True)
            return Response(data=serializer.data, status=200)
        else:
            return Response(status=204)

    def post(self, request):
        """Create a new answer"""
        user = self.request.user
        skipped = False
        duration = self.request.data['duration'] if 'duration' in self.request.data else 0

        if user is None or user == '':
            return Response(data='User not defined', status=400)
        if 'question' in self.request.data and self.request.data['question'] != '':
            filter_dict = {'id': self.request.data['question']}
            question = Question.objects.filter(**filter_dict)[0]
            if question is None:
                return Response(data='Question does not exist', status=400)
        else:
            return Response(data='Question not defined', status=400)
        if 'answers' in self.request.data and self.request.data['answers'] != '':
            answers = self.request.data['answers']
        else:
            if 'skipped' in self.request.data and not bool(self.request.data['skipped']):
                return Response(data='Answers not defined', status=400)
            else:
                answers = ""
                skipped = True

        answer=models.Answer.objects.get_or_create(
            user_profile_id=user.id,
            question=question,
            answers=answers,
            duration=duration,
            skipped=skipped,
            correct=False
        )[0]

        if 'comment' in self.request.data and self.request.data['comment'] != '':
            answer.comment = self.request.data['comment']

        answer.performCorrection()

        serializer = serializers.AnswerSerializer(answer)
        return Response(data=serializer.data, status=201)


