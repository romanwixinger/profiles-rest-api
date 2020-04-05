from rest_framework import serializers

from profiles_api.answer.answer_model import Answer


class AnswerSerializer(serializers.ModelSerializer):
    """Serializes answers"""

    class Meta:
        model = Answer
        fields = ('id', 'user_profile', 'created_on', 'question',
                  'duration', 'answers', 'correct', 'skipped', 'comment')
        extra_kwargs = {'user_profile': {'read_only': True}}
