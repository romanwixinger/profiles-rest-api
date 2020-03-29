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


class UserProfileQuestionViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating question items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.QuestionFeedItemSerializer
    queryset = models.QuestionFeedItem.objects.all()
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
        questions = models.QuestionFeedItem.objects.filter(**filter_dict)

        if start is not None:
            questions = questions[min(abs(int(start)), questions.count()):]
        if number is not None:
            questions = questions[:max(0, min(int(number), questions.count()))]

        return questions




class TopicViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating topics"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.TopicSerializer
    queryset = models.Topic.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)


class SubtopicViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating subtopics"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.SubTopicSerializer
    queryset = models.Subtopic.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)

    def get_queryset(self):
        """Retrieve only subtopic with certain topic"""
        topic = self.request.query_params.get('topic', None)
        start = self.request.query_params.get('start', None)
        number = self.request.query_params.get('number', None)

        """Return subtopics"""
        if topic is not None:
            filter_dict = {'topic__name': topic}
            subtopics = models.Subtopic.objects.filter(**filter_dict)
        else:
            subtopics = models.Subtopic.objects.all()

        if start is not None:
            subtopics = subtopics[min(abs(int(start)), subtopics.count()):]

        if number is not None:
            subtopics = subtopics[:max(0, min(int(number), subtopics.count()))]

        return subtopics


class CustomSubtopicView(APIView):

    def get(self, request):
        return Response(status=418)

    def post(self, request):
        topic_name = request.data['topic']
        if topic_name is None or topic_name == '':
            return Response(data='Topic not defined', status=400)

        user_profile_id = request.user.id

        if user_profile_id is None or user_profile_id == '':
            return Response(data='User not defined', status=400)
        else:
            topic = models.Topic.objects.get_or_create(
                name=topic_name,
                user_profile_id=request.user.id
            )[0]

            subtopic = models.Subtopic.objects.get_or_create(
                topic=topic,
                name=request.data['name'],
                html=request.data['html'],
                user_profile_id=request.user.id
            )[0]

            return Response(data=subtopic, status=200)
