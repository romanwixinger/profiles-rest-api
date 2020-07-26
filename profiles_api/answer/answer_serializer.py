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
        extra_kwargs = {'user_profile': {'read_only': True}, 'correct': {'required': False}, 'duration': {'required': False}}


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

        if 'answers' in data:
            return data
        if 'skipped' in data and data['skipped']:
            return data

        raise serializers.ValidationError("No answer was provided and the question was not skipped.")

    def create(self, validated_data):
        """Creates an answer"""

        user = UserProfile.objects.filter(**{'id': validated_data['user_id']})[0]

        filter_dict = {'id': validated_data['question']}
        question = Question.objects.filter(**filter_dict)[0] \
            if Question.objects.filter(**filter_dict).count() > 0 else None
        if question is None:
            raise ValueError("The question for this answer does not exist.")

        args = {'question': question, 'user_profile': user}
        if 'answers' in validated_data:
            args['answers'] = validated_data['answers']
        opt_args = {key: validated_data[key] for key in ['skipped', 'correct', 'comment'] if key in validated_data}

        number = len(Answer.objects.filter(**args))
        if number > 1:
            raise LookupError
        if number == 1:
            Answer.objects.filter(**args).update(**opt_args)

        answer = Answer.objects.get_or_create(**args, defaults=opt_args)[0]
        return answer


class AnswerPatchDeserializer(serializers.Serializer):
    """Deserializes answer patches"""

    duration = serializers.FloatField(required=False, default=0)
    answers = serializers.CharField(max_length=1024, required=False, allow_blank=False)
    correct = serializers.BooleanField(required=False, allow_null=False)
    skipped = serializers.BooleanField(required=False, default=False)
    comment = serializers.CharField(max_length=1024, required=False, allow_blank=False)

    def validate(self, data):
        """Validates the data"""
        return data

    def update(self, instance, validated_data):
        """Update an answer"""

        if 'answers' in validated_data:
            instance.answers = validated_data['answers']
        if 'duration' in validated_data:
            instance.duration = validated_data['duration']
        if 'correct' in validated_data:
            instance.correct = validated_data['correct']
        if 'skipped' in validated_data:
            instance.skipped = validated_data['skipped']
        if 'comment' in validated_data:
            instance.comment = validated_data['comment']

        return instance
