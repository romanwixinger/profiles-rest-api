from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from profiles_api import permissions

from profiles_api.proficiency.proficiency_model import Proficiency
from profiles_api.proficiency.proficiency_serializer import ProficiencySerializer


class ProficiencyView(APIView):
    """Custom view for Subtopic"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def get(self, request):
        """Retrieve only certain subtopics"""

        #query_params_dict = self.request.query_params.dict()
        #proficiencies = ProficiencyService.search_subtopics(query_params_dict)

        proficiencies = Proficiency.objects.all()

        if len(proficiencies) > 0:
            serializer = ProficiencySerializer(proficiencies, many=True)
            return Response(data=serializer.data, status=200)
        else:
            return Response(status=204)
