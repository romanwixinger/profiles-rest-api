from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_api import permissions

from profiles_api.answer.answer_serializer import AnswerSerializer, AnswerDeserializer
from profiles_api.answer.answer_model import Answer
from profiles_api.answer.answer_service import AnswerService


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

        query_params_dict = self.request.query_params.dict()
        if 'user_id' in query_params_dict:
            return Response(status=status.HTTP_403_FORBIDDEN)
        query_params_dict['user_id'] = self.request.user.id
        answers = AnswerService.search_answers(query_params_dict)

        if len(answers) > 0:
            serializer = AnswerSerializer(answers, many=True)
            return Response(data=serializer.data, status=200)

        return Response(status=204)

    def post(self, request):
        """Create a new answer"""

        user = self.request.user
        if user is None or user.id == '':
            return Response(data='User not defined', status=400)

        deserializer = AnswerDeserializer(data=request.data)

        if deserializer.is_valid():
            validated_data = deserializer.validated_data
            validated_data['user_id'] = user.id

            try:
                answer = deserializer.create(validated_data)
            except ValueError:
                return Response(data={"question": "The question for this answer does not exist."}, status=400)

            AnswerService.perform_correction(answer)

            answer.save()

            serializer = AnswerSerializer(answer)
            return Response(data=serializer.data, status=201)

        else:
            return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)
