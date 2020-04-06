from rest_framework import serializers

from django.db import models

from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.topic.topic_model import Topic


class SubtopicDeserializer(serializers.Serializer):
    """Deserializes subtopics"""

    name = serializers.CharField(max_length=255)
    html = serializers.CharField(max_length=1024, allow_blank=True)
    topic = serializers.CharField(max_length=255)

    def create(self, validated_data):

        if validated_data['topic'] == '':
            serializers.ValidationError("Topic not defined.")
            return None

        user_id = validated_data['user_id']

        if user_id is None or user_id == '':
            return serializers.ValidationError("User not defined.")

        topic = Topic.objects.get_or_create(
            name=validated_data['topic'],
            user_profile_id=user_id
        )[0]

        subtopic = Subtopic.objects.get_or_create(
            topic=topic,
            name=validated_data['name'],
            html=validated_data['html'],
            user_profile_id=user_id
        )[0]

        return subtopic


class SubtopicSerializer(serializers.ModelSerializer):
    """Serializes subtopics"""

    class Meta:
        model = Subtopic
        fields = ('id', 'user_profile', 'name', 'html', 'topic')
        extra_kwargs = {'user_profile': {'read_only': True}}
