from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from profiles_api import permissions

from profiles_api.theory_page.theory_page_serializer import TheoryPageSerializer, TheoryPageDeserializer
from profiles_api.theory_page.theory_page_model import TheoryPage
from profiles_api.theory_page.theory_page_service import get_recommended_theory_pages


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

        _ = get_recommended_theory_pages(request.user)

        theory_page_id = self.request.query_params.get('id', None)
        title = self.request.query_params.get('title', None)

        filter_dict = {}
        if theory_page_id is not None and theory_page_id.isdigit():
            print("true")
            filter_dict['id'] = int(theory_page_id)
        if title is not None:
            filter_dict['title'] = title

        theory_pages = TheoryPage.objects.filter(**filter_dict)

        start = self.request.query_params.get('start', None)
        number = self.request.query_params.get('number', None)

        if start is not None:
            theory_pages = theory_pages[min(abs(int(start)), theory_pages.count()):]
        if number is not None:
            theory_pages = theory_pages[:max(0, min(int(number), theory_pages.count()))]

        if theory_pages.count() == 0:
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
            theory_page = deserializer.create(validated_data)

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

        theory_pages_id = get_recommended_theory_pages(request.user)
        theory_pages = TheoryPage.objects.filter(id__in=theory_pages_id)
        if theory_pages is None:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        start = self.request.query_params.get('start', None)
        number = self.request.query_params.get('number', None)

        if start is not None:
            theory_pages = theory_pages[min(abs(int(start)), theory_pages.count()):]
        if number is not None:
            theory_pages = theory_pages[:max(0, min(int(number), theory_pages.count()))]

        if theory_pages.count() == 0:
            return Response(status=204)

        serializer = TheoryPageSerializer(theory_pages, many=True)
        return Response(data=serializer.data, status=200)

