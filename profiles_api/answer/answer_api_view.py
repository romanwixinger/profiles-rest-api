from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_api import permissions

from profiles_api.answer.answer_serializer import AnswerSerializer
from profiles_api.answer.answer_model import Answer
from profiles_api.question.question_model import Question


class AnswerViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating answers"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
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
        answers = Answer.objects.filter(**filter_dict)

        if start is not None:
            answers =answers[min(abs(int(start)), answers.count()):]
        if number is not None:
            answers = answers[:max(0, min(int(number), answers.count()))]

        if answers.count() > 0:
            serializer = AnswerSerializer(answers, many=True)
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

        answer = Answer.objects.get_or_create(
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

        serializer = AnswerSerializer(answer)
        return Response(data=serializer.data, status=201)
