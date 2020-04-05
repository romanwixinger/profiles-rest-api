from rest_framework import serializers

from profiles_api.question.question_model import Question


class QuestionSerializer(serializers.ModelSerializer):
    """Serializes questions"""

    class Meta:
        model = Question
        fields = ('id', 'created_on', 'topic', 'subtopic', 'dependencies',
                  'question', 'correctAnswers', 'appendix', 'hint', 'imageSrc',
                  'user_profile', 'validation')
        extra_kwargs = {'user_profile': {'read_only': True}, 'appendix': {'required': False}}
