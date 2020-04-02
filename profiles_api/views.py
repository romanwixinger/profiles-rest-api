from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from rest_framework.authtoken.models import Token #Get user_profile from corresponding token

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


class QuestionViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating question items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.QuestionSerializer
    queryset = models.Question.objects.all()
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
        questions = models.Question.objects.filter(**filter_dict)

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
        topic_id = self.request.query_params.get('topic_id', None)
        start = self.request.query_params.get('start', None)
        number = self.request.query_params.get('number', None)

        """Return subtopics"""
        if topic is not None:
            filter_dict = {'topic__name': topic}
            subtopics = models.Subtopic.objects.filter(**filter_dict)
        elif topic_id is not None:
            filter_dict = {'topic__id': topic_id}
            subtopics = models.Subtopic.objects.filter(**filter_dict)
        else:
            subtopics = models.Subtopic.objects.all()

        if start is not None:
            subtopics = subtopics[min(abs(int(start)), subtopics.count()):]

        if number is not None:
            subtopics = subtopics[:max(0, min(int(number), subtopics.count()))]

        return subtopics


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
        questions = models.Question.objects.filter(**filter_dict)

        if start is not None:
            questions = questions[min(abs(int(start)), questions.count()):]
        if number is not None:
            questions = questions[:max(0, min(int(number), questions.count()))]

        serializer = serializers.QuestionSerializer(questions, many=True)
        return Response(data=serializer.data, status=200)

    def post(self, request):
        user = self.request.user
        try:
            question_question = request.data['question']
        except:
            return Response(data='Question is not defined', status=400)
        try:
            correctAnswers = request.data['correctAnswers']
        except:
            return Response(data='Answer is not defined', status=400)
        try:
            topic_name = request.data['topic']
        except:
            topic_name = None
        try:
            topic_id = request.data['topic_id']
        except:
            topic_id = None
        try:
            subtopic_name = request.data['subtopic']
        except:
            subtopic_name = None
        try:
            subtopic_id = request.data['subtopic_id']
        except:
            subtopic_id = None

        # Check user, question, answer, topic and subtopic
        if user is None or user.id == '':
            return Response(data='User not defined', status=400)
        if question_question is None or question_question == '':
            return Response(data='Question not defined', status=400)
        if correctAnswers is None or correctAnswers == '':
            return Response(data='Answer not defined', status=400)
        if topic_name is None or topic_name == '':
            if topic_id is None or topic_id == '':
                return Response(data='Topic not defined', status=400)
            else:
                filter_dict = {'id': topic_id}
                topic = models.Topic.objects.filter(**filter_dict)[0]
        else:
            topic = models.Topic.objects.get_or_create(
                name=topic_name,
                user_profile_id=user.id
            )[0]
        if subtopic_name is None or subtopic_name == '':
            if subtopic_id is None or subtopic_id == '':
                return Response(data='Subtopic not defined', status=400)
            else:
                filter_dict = {'id': subtopic_id}
                subtopic = models.Subtopic.objects.filter(**filter_dict)[0]
        else:
            subtopic = models.Subtopic.objects.get_or_create(
                name=subtopic_name,
                topic=topic,
                user_profile_id=user.id
            )[0]

        # Create questions
        question = models.Question.objects.get_or_create(
            user_profile_id=user.id,
            topic=topic,
            subtopic=subtopic,
            question=question_question,
            correctAnswers=correctAnswers
        )[0]

        try:
            dependencies = request.data['dependencies']
        except:
            dependencies = None
        try:
            dependencies_id = request.data['dependencies_id']
        except:
            dependencies_id = None
        try:
            validation = request.data['validation']
        except:
            validation = None
        try:
            appendix = request.data['appendix']
        except:
            appendix = None
        try:
            hint = request.data['hint']
        except:
            hint = None
        try:
            imageSrc = request.data['imageSrc']
        except:
            imageSrc = None

        if dependencies is not None and dependencies != "":
            dependencies_string = dependencies.split(',')
            for dependency_string in dependencies_string:
                filter_dict = {'name': dependency_string}
                try:
                    dependency = models.Subtopic.objects.filter(**filter_dict)[0]
                    question.dependencies.add(dependency)
                except:
                    pass

        if dependencies_id is not None and dependencies_id != "":
            dependencies_string = dependencies_id.split(',')
            for dependency_string in dependencies_string:
                filter_dict = {'id': dependency_string}
                try:
                    dependency = models.Subtopic.objects.filter(**filter_dict)[0]
                    question.dependencies.add(dependency)
                except:
                    pass

        if validation is not None and validation != '':
            question.validation = validation
        if appendix is not None and appendix != '':
            question.appendix = appendix
        if hint is not None and hint != '':
            question.hint = hint
        if imageSrc is not None and imageSrc != '':
            question.imageSrc = imageSrc

        serializer = serializers.QuestionSerializer(question)
        return Response(data=serializer.data, status=201)


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
            subtopics = models.Subtopic.objects.filter(**filter_dict)
        elif topic_id is not None:
            filter_dict = {'topic__id': topic_id}
            subtopics = models.Subtopic.objects.filter(**filter_dict)
        else:
            subtopics = models.Subtopic.objects.all()

        if start is not None:
            subtopics = subtopics[min(abs(int(start)), subtopics.count()):]

        if number is not None:
            subtopics = subtopics[:max(0, min(int(number), subtopics.count()))]

        serializer = serializers.SubTopicSerializer(subtopics, many=True)

        return Response(data=serializer.data, status=200)

    def post(self, request):
        topic_name = request.data['topic']
        if topic_name is None or topic_name == '':
            return Response(data='Topic not defined', status=400)

        user = self.request.user

        if user is None or user.id == '':
            return Response(data='User not defined', status=400)
        else:
            topic = models.Topic.objects.get_or_create(
                name=topic_name,
                user_profile_id=user.id
            )[0]

            subtopic = models.Subtopic.objects.get_or_create(
                topic=topic,
                name=request.data['name'],
                html=request.data['html'],
                user_profile_id=user.id
            )[0]

            serializer = serializers.SubTopicSerializer(subtopic)

            return Response(data=serializer.data, status=201)


class TopicView(APIView):
    """Custom view for topics"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def get(self, request):
        """Retrieve only certain topics"""
        start = self.request.query_params.get('start', None)
        number = self.request.query_params.get('number', None)

        topics = models.Topic.objects.all()

        if start is not None:
            topics = topics[min(abs(int(start)), topics.count()):]

        if number is not None:
            topics = topics[:max(0, min(int(number), topics.count()))]

        serializer = serializers.TopicSerializer(topics, many=True)

        return Response(data=serializer.data, status=200)

    def post(self, request):
        topic_name = request.data['topic']
        if topic_name is None or topic_name == '':
            return Response(data='Topic not defined', status=400)

        user = self.request.user

        if user is None or user.id == '':
            return Response(data='User not defined', status=400)
        else:
            topic = models.Topic.objects.get_or_create(
                name=topic_name,
                user_profile_id=user.id
            )[0]

        serializer = serializers.TopicSerializer(topic)
        return Response(data=serializer.data, status=201)
