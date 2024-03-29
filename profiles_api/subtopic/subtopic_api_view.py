from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from profiles_api import permissions

from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.question.question_model import Question

from profiles_api.subtopic.subtopic_serializer import SubtopicSerializer, SubtopicDeserializer
from profiles_api.subtopic.subtopic_service import SubtopicService


class SubtopicViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating subtopics"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = SubtopicSerializer
    queryset = Subtopic.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)


class CustomSubtopicView(APIView):
    """Custom view for Subtopic"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def get(self, request):
        """Retrieve only certain subtopics"""

        query_params_dict = self.request.query_params.dict()
        subtopics = Subtopic.search_subtopics(query_params_dict)

        if 'update' in query_params_dict:
            for subtopic in subtopics:
                Question.update_difficulty(subtopic=subtopic, new_answer=False, force_update=True)

        if len(subtopics) > 0:
            serializer = SubtopicSerializer(subtopics, many=True)
            return Response(data=serializer.data, status=200)
        else:
            return Response(status=204)

    def post(self, request):
        """Create a new subtopic. Additionally a new topic is created if necessary"""

        deserializer = SubtopicDeserializer(data=request.data)

        if deserializer.is_valid():
            deserializer.validated_data['user_id'] = self.request.user.id
            subtopic = deserializer.create(deserializer.validated_data)
            subtopic.save()

            serializer = SubtopicSerializer(subtopic)
            return Response(data=serializer.data, status=201)

        return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendedSubtopicView(APIView):
    """Custom view for getting recommended subtopics"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def get(self, request):
        """Retrieve recommended subtopics"""

        query_params_dict = self.request.query_params.dict()
        args = {'number': int(query_params_dict['number'])} if 'number' in query_params_dict else {}
        subtopic_id_list = SubtopicService.recommended_subtopics(user=self.request.user, **args)
        subtopics = Subtopic.get_subtopics(subtopic_id_list)

        if len(subtopics) > 0:
            serializer = SubtopicSerializer(subtopics, many=True)
            return Response(data=serializer.data, status=200)
        else:
            return Response(status=204)
