from rest_framework import serializers

from profiles_api.topic.topic_model import Topic


class TopicSerializer(serializers.ModelSerializer):
    """Serializes topics"""

    class Meta:
        model = Topic
        fields = ('id', 'user_profile', 'name')
        extra_kwargs = {'user_profile': {'read_only': True}}

