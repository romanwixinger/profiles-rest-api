from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_api import permissions

from profiles_api.question.question_serializer import QuestionSerializer
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.question.question_model import Question
from profiles_api.topic.topic_model import Topic


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
        try:
            question_question = request.data['question']
        except:
            return Response(data='Question is not defined', status=400)
        try:
            correctAnswers = request.data['correctAnswers']
        except:
            return Response(data='Answer is not defined', status=400)

        topic_name = request.data['topic'] if 'topic' in request.data else None
        topic_id = request.data['topic_id'] if 'topic_id' in request.data else None
        subtopic_name = request.data['subtopic'] if 'subtopic' in request.data else None
        subtopic_id = request.data['subtopic_id'] if 'subtopic_id' in request.data else None

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
                topic = Topic.objects.filter(**filter_dict)[0]
        else:
            topic = Topic.objects.get_or_create(
                name=topic_name,
                user_profile_id=user.id
            )[0]
        if subtopic_name is None or subtopic_name == '':
            if subtopic_id is None or subtopic_id == '':
                return Response(data='Subtopic not defined', status=400)
            else:
                filter_dict = {'id': subtopic_id}
                subtopic = Subtopic.objects.filter(**filter_dict)[0]
        else:
            subtopic = Subtopic.objects.get_or_create(
                name=subtopic_name,
                topic=topic,
                user_profile_id=user.id
            )[0]

        # Create questions
        question = Question.objects.get_or_create(
            user_profile_id=user.id,
            topic=topic,
            subtopic=subtopic,
            question=question_question,
            correctAnswers=correctAnswers
        )[0]

        dependencies = request.data['dependencies'] if 'dependencies' in request.data else None
        dependencies_id = request.data['dependencies_id'] if 'dependencies_id' in request.data else None
        validation = request.data['validation'] if 'validation' in request.data else None
        appendix = request.data['appendix'] if 'appendix' in request.data else None
        hint = request.data['hint'] if 'hint' in request.data else None
        imageSrc = request.data['imageSrc'] if 'imageSrc' in request.data else None

        if dependencies is not None and dependencies != "":
            dependencies_string = dependencies.split(';')
            for dependency_string in dependencies_string:
                filter_dict = {'name': dependency_string}
                try:
                    dependency = Subtopic.objects.filter(**filter_dict)[0]
                    question.dependencies.add(dependency)
                except:
                    pass

        if dependencies_id is not None and dependencies_id != "":
            dependencies_string = dependencies_id.split(',')
            for dependency_string in dependencies_string:
                filter_dict = {'id': dependency_string}
                try:
                    dependency = Subtopic.objects.filter(**filter_dict)[0]
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

        serializer = QuestionSerializer(question)
        return Response(data=serializer.data, status=201)
