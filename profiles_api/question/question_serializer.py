from rest_framework import serializers

from profiles_api.question.question_model import Question
from profiles_api.topic.topic_model import Topic
from profiles_api.subtopic.subtopic_model import Subtopic


class QuestionDeserializer(serializers.Serializer):
    """Deserializes questions"""

    subtopic = serializers.CharField(max_length=255, required=False, allow_blank=False)
    subtopic_id = serializers.IntegerField(required=False, allow_null=False)
    dependencies = serializers.CharField(max_length=255, required=False, allow_blank=False)
    dependencies_id = serializers.CharField(max_length=255, required=False, allow_blank=False)
    question = serializers.CharField(max_length=1024, required=True, allow_blank=False)
    correctAnswers = serializers.CharField(max_length=1024, required=True, allow_blank=False)
    validation_type = serializers.ChoiceField([('standardValidation', ''),
                                               ('multipleStrings', 'multipleStrings'),
                                               ('singleFraction', 'singleFraction')],
                                              default='standardValidation',
                                              required=False,
                                              allow_blank=False)
    appendix = serializers.CharField(max_length=1024, required=False, allow_blank=False)
    hint = serializers.CharField(max_length=1024, required=False, allow_blank=False)
    imageSrc = serializers.CharField(max_length=1024, required=False, allow_blank=False)
    set_difficulty = serializers.ChoiceField([(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                                             default=0,
                                             required=False,
                                             allow_blank=False)

    def validate(self, data):
        """Validate if topic and subtopic are given"""

        if 'subtopic' not in data and 'subtopic_id' not in data:
            raise serializers.ValidationError("Subtopic must be defined.")

        return data

    def create(self, validated_data):
        """Create a new question from the validated data"""

        filter_dict = {}
        if 'subtopic_id' in validated_data:
            filter_dict['id'] = validated_data['subtopic_id']
        if 'subtopic' in validated_data:
            filter_dict['name'] = validated_data['subtopic']

        subtopics = Subtopic.objects.filter(**filter_dict)
        if subtopics.count() > 0:
            subtopic = subtopics[0]
        else:
            raise ValueError("The subtopic is not defined.")

        topics = Topic.objects.filter(**{'name': subtopic.topic.name})
        if topics.count() > 0:
            topic = topics[0]
        else:
            raise ValueError("The topic of this subtopic does not exist.")

        args = {key: validated_data[key] for key in ['question', 'correctAnswers', 'difficulty', 'validation_type',
                                                     'appendix', 'hint', 'imageSrc'] if key in validated_data}
        question = Question.objects.get_or_create(
            user_profile_id=validated_data['user_id'],
            topic=topic,
            subtopic=subtopic,
            set_difficulty=validated_data['set_difficulty'],
            **args
        )[0]

        for (key, field) in zip(['dependencies', 'dependencies_id'], ['name', 'id']):
            if key not in validated_data:
                continue

            for dependency_string in validated_data[key].split(';'):
                try:
                    dependency = Subtopic.objects.filter(**{field: dependency_string})[0]
                    question.dependencies.add(dependency)
                except LookupError:
                    pass

        return question


class QuestionSerializer(serializers.ModelSerializer):
    """Serializes questions"""

    class Meta:
        model = Question
        fields = ('id', 'created_on', 'topic', 'subtopic', 'dependencies',
                  'question', 'correctAnswers', 'appendix', 'hint', 'imageSrc',
                  'user_profile', 'validation_type', 'difficulty', 'set_difficulty')
        extra_kwargs = {'user_profile': {'read_only': True}, 'appendix': {'required': False}}
