from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_api import permissions

from profiles_api.question.question_serializer import QuestionSerializer, QuestionDeserializer
from profiles_api.question.question_model import Question
from profiles_api.question.question_service import QuestionService


class QuestionViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating question items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
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

        query_params_dict = self.request.query_params.dict()
        questions = Question.search_questions(query_params_dict)

        question_id_list = [question.id for question in questions]
        QuestionService.update_facilities(question_id_list)

        if len(questions) == 0:
            return Response(status=204)

        serializer = QuestionSerializer(questions, many=True)
        return Response(data=serializer.data, status=200)

    def post(self, request):
        """Create a new question. Additionally a new topic and subtopic is created if necessary"""

        user = self.request.user
        deserializer = QuestionDeserializer(data=request.data)

        if deserializer.is_valid():
            deserializer.validated_data['user_id'] = user.id
            question = deserializer.create(deserializer.validated_data)
            question.save()

            serializer = QuestionSerializer(question)
            return Response(data=serializer.data, status=201)

        return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)
