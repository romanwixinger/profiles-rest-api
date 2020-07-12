from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_api import permissions

from profiles_api.theory_page.theory_page_serializer import TheoryPageSerializer, TheoryPageDeserializer
from profiles_api.theory_page.theory_page_model import TheoryPage

from profiles_api.topic.topic_service import TopicService
from profiles_api.theory_page.theory_page_service import TheoryPageService


class TheoryPageViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating theory pages"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = TheoryPageSerializer
    queryset = TheoryPage.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)


class TheoryPageView(APIView):
    """Get and create theory pages"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def get(self, request):
        """Get certain theory pages"""

        query_params_dict = self.request.query_params.dict()
        theory_pages = TheoryPageService.search_theory_pages(query_params_dict)

        if len(theory_pages) == 0:
            return Response(status=204)

        serializer = TheoryPageSerializer(theory_pages, many=True)
        return Response(data=serializer.data, status=200)

    def post(self, request):
        """Create a new theory page"""

        deserializer = TheoryPageDeserializer(data=request.data)

        if deserializer.is_valid():

            user = self.request.user
            validated_data = deserializer.validated_data
            validated_data['user_id'] = user.id

            try:
                theory_page = deserializer.create(validated_data)
            except ValueError:
                return Response(
                    data={"topic_id": "The given topic, subtopic or test does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if theory_page is None:
                return Response(
                    deserializer.errors,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            serializer = TheoryPageSerializer(theory_page)
            return Response(data=serializer.data, status=201)

        return Response(
            deserializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class RecommendedTheoryPageView(APIView):
    """Get recommended theory pages"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def get(self, request):
        """Get recommended theory pages"""

        theory_page_id_list = TheoryPageService.recommended_theory_pages(request.user)
        theory_pages_list = TheoryPageService.get_theory_pages(theory_page_id_list)

        if len(theory_pages_list) == 0:
            Response(status=204)

        TopicService.select_items(items=theory_pages_list, query_params_dict=self.request.query_params.dict())

        if len(theory_pages_list) == 0:
            return Response(status=204)

        serializer = TheoryPageSerializer(theory_pages_list, many=True)
        return Response(data=serializer.data, status=200)

