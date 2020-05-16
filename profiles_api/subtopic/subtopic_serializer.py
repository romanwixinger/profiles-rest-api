from rest_framework import serializers

from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.topic.topic_model import Topic


class SubtopicDeserializer(serializers.Serializer):
    """Deserializes subtopics"""

    name = serializers.CharField(max_length=255, required=True, allow_blank=False)
    html = serializers.CharField(max_length=8191, required=False, allow_blank=False)
    topic = serializers.CharField(max_length=255, required=True, allow_blank=False)

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

        if 'html' in validated_data:
            subtopic = Subtopic.objects.get_or_create(
                topic=topic,
                name=validated_data['name'],
                html=validated_data['html'],
                user_profile_id=user_id
            )[0]

        else:
            subtopic = Subtopic.objects.get_or_create(
                topic=topic,
                name=validated_data['name'],
                user_profile_id=user_id
            )[0]

        return subtopic


class SubtopicSerializer(serializers.ModelSerializer):
    """Serializes subtopics"""

    class Meta:
        model = Subtopic
        fields = ('id', 'user_profile', 'name', 'html', 'topic')
        extra_kwargs = {'user_profile': {'read_only': True}}
