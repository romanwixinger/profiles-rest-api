from rest_framework import serializers

from django.conf import settings

from profiles_api.topic.topic_model import Topic
from profiles_api import models


class TopicSerializer(serializers.ModelSerializer):
    """Serializes topics"""

    class Meta:
        model = Topic
        fields = ('id', 'user_profile', 'name')
        extra_kwargs = {'user_profile': {'read_only': True}}


class TopicDeserializer(serializers.Serializer):
    """Deserializes topics"""

    name = serializers.CharField(max_length=255)

