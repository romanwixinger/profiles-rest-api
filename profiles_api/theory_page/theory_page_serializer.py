from rest_framework import serializers

from profiles_api.theory_page.theory_page_model import TheoryPage


class TheoryPageSerializer(serializers.ModelSerializer):
    """Serializes theory page"""

    class Meta:
        model = TheoryPage
        fields = ('id', 'user_profile', 'created_on', 'updated_on', 'topic', 'subtopic', 'title', 'html', 'test')
        extra_kwargs = {'user_profile': {'read_only': True}}
