from rest_framework import serializers

from profiles_api.answer.answer_model import Answer
from profiles_api.question.question_model import Question

from profiles_api.models import UserProfile


class AnswerSerializer(serializers.ModelSerializer):
    """Serializes answers"""

    class Meta:
        model = Answer
        fields = ('id', 'user_profile', 'created_on', 'question',
                  'duration', 'answers', 'correct', 'skipped', 'comment')
        extra_kwargs = {'user_profile': {'read_only': True}, 'correct': {'required': False}}


class AnswerDeserializer(serializers.Serializer):
    """Deserializes answers"""

    question = serializers.IntegerField(required=True)
    duration = serializers.FloatField(required=False, default=0)
    answers = serializers.CharField(max_length=1024, required=False, allow_blank=False)

    correct = serializers.BooleanField(required=False, allow_null=False)
    skipped = serializers.BooleanField(required=False, default=False)
    comment = serializers.CharField(max_length=1024, required=False, allow_blank=False)

    def validate(self, data):
        """Validates the data: Checks whether an answer was given or the question was skipped"""

        if 'answers' in data and data['answers'] != '':
            return data
        if 'skipped' in data and data['skipped']:
            return data

        raise serializers.ValidationError("No answer was provided and the question was not skipped.")

    def create(self, validated_data):
        """Creates an answer"""

        filter_dict = {'id': validated_data['user_id']}
        user_profile = UserProfile.objects.filter(**filter_dict)[0]

        filter_dict = {'id': validated_data['question']}
        question = Question.objects.filter(**filter_dict)[0] \
            if Question.objects.filter(**filter_dict).count() > 0 else None
        if question is None:
            raise ValueError("The question for this answer does not exist.")

        answer = Answer(
            question=question,
            user_profile=user_profile
        )
        if 'duration' in validated_data:
            answer.duration = validated_data['duration']
        else:
            answer.duration = 0
        if 'answers' in validated_data and validated_data['answers'] != '':
            answer.answers = validated_data['answers']
        if 'skipped' in validated_data:
            answer.skipped = validated_data['skipped']
        if 'correct' in validated_data:
            answer.correct = validated_data['correct']
        if 'comment' in validated_data and validated_data['comment'] != '':
            answer.comment = validated_data['comment']

        return answer





