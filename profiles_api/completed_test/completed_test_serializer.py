from rest_framework import serializers

from profiles_api.completed_test.completed_test_model import CompletedTest
from profiles_api.answer.answer_serializer import AnswerDeserializer
from profiles_api.models import UserProfile

from profiles_api.test.test_service import TestService
from profiles_api.answer.answer_service import AnswerService


class CompletedTestDeserializer(serializers.Serializer):
    """Deserializes completed tests"""

    answers = serializers.JSONField(required=False, allow_null=False)
    state = serializers.CharField(max_length=255, required=True, allow_null=False)
    duration = serializers.DecimalField(max_digits=8, decimal_places=2, default=0)  # in seconds
    comment = serializers.CharField(max_length=1024, required=False, allow_blank=False)
    test = serializers.IntegerField(required=True, allow_null=False)

    def validate(self, data):
        """Validates the completed test: Checks if the answers are valid"""

        if 'answers' in data:
            answers_list = data['answers']

            for answer_item in answers_list:
                answer_deserializer = AnswerDeserializer(data=answer_item)
                if not answer_deserializer.is_valid():
                    raise serializers.ValidationError('Invalid answers given.')
        return data

    def create(self, validated_data):
        """Create a new completed test"""

        user = UserProfile.objects.filter(**{'id': validated_data['user_id']})[0]

        test_id = validated_data['test']
        tests = TestService.search_tests(query_params_dict={'id': test_id})

        test = tests[0] if len(tests) > 0 else None
        if test is None:
            raise ValueError

        validated_data['duration'] = 0 if 'duration' not in validated_data else 0

        args = {key: validated_data[key] for key in ['state', 'duration', 'comment'] if key in validated_data}

        completed_test = CompletedTest.objects.get_or_create(
            user_profile=user,
            test=test,
            defaults=args
        )[0]

        if 'answers' in validated_data:
            answers_list = validated_data['answers']

            for answer_item in answers_list:
                answer_deserializer = AnswerDeserializer(data=answer_item)
                if not answer_deserializer.is_valid():
                    return None

                answer_validated_data = answer_deserializer.validated_data
                answer_validated_data['user_id'] = validated_data['user_id']

                try:
                    answer_query = completed_test.answers.filter(**{'question': answer_validated_data['question']})
                    answer = answer_deserializer.update(answer_query[0], answer_validated_data) \
                        if answer_query.count() > 0 else answer_deserializer.create(answer_validated_data)

                except ValueError:
                    raise ValueError("The question for this answer does not exist.")

                if answer is None:
                    return None

                AnswerService.perform_correction(answer)
                answer.save()

                completed_test.answers.add(answer)

        completed_test.save()

        return completed_test


class CompletedTestSerializer(serializers.ModelSerializer):
    """Serializes completed tests"""

    class Meta:
        model = CompletedTest
        fields = ('id', 'user_profile', 'answers', 'state', 'created_on',
                  'updated_on', 'duration', 'comment', 'recommendedSubtopics', 'test')
        extra_kwargs = {'user_profile': {'read_only': True}}


class CompletedTestPatchDeserializer(serializers.Serializer):
    """Deserializes parts of completed tests"""

    answers = serializers.JSONField(required=False, allow_null=False)
    state = serializers.CharField(max_length=255, required=False, allow_null=False)
    duration = serializers.DecimalField(max_digits=8, decimal_places=2, default=0, required=False)  # in seconds
    comment = serializers.CharField(max_length=1024, required=False, allow_blank=False)

    def validate(self, data):
        """Validates the completed test: Checks if the answers are valid"""

        if 'answers' in data:
            answers_list = data['answers']

            for answer_item in answers_list:
                answer_deserializer = AnswerDeserializer(data=answer_item)
                if not answer_deserializer.is_valid():
                    raise serializers.ValidationError('Invalid answers given.')
        return data

    def update(self, instance, validated_data):
        """Update an instance of a completed test"""
        
        if 'state' in validated_data:
            instance.state = validated_data['state']
        if 'duration' in validated_data:
            instance.duration = validated_data['duration']
        if 'comment' in validated_data:
            instance.state = validated_data['comment']

        if 'answers' in validated_data:
            answers_list = validated_data['answers']

            for answer_item in answers_list:
                answer_deserializer = AnswerDeserializer(data=answer_item)
                if not answer_deserializer.is_valid():
                    return None

                answer_validated_data = answer_deserializer.validated_data
                answer_validated_data['user_id'] = validated_data['user_id']

                try:
                    answer_query = instance.answers.filter(**{'question': answer_validated_data['question']})
                    answer = answer_deserializer.update(answer_query[0], answer_validated_data) \
                        if answer_query.count() > 0 else answer_deserializer.create(answer_validated_data)

                except ValueError:
                    raise ValueError("The question for this answer does not exist.")

                if answer is None:
                    return None

                AnswerService.perform_correction(answer)
                answer.save()

                instance.answers.add(answer)

        instance.save()
        return instance
