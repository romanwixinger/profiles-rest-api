from rest_framework import serializers

from profiles_api.subtopic.subtopic_model import Subtopic


class SubTopicSerializer(serializers.ModelSerializer):
    """Serializes subtopics"""

    class Meta:
        model = Subtopic
        fields = ('id', 'user_profile', 'name', 'html', 'topic')
        extra_kwargs = {'user_profile': {'read_only': True}}
