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

        subtopic_name = data['subtopic'] if ('subtopic' in data and data['subtopic'] != '') else None
        subtopic_id = data['subtopic_id'] if ('subtopic_id' in data and data['subtopic_id'] != '') else None

        if subtopic_name is None and subtopic_id is None:
            raise serializers.ValidationError("Subtopic must be defined.")

        return data

    def create(self, validated_data):
        """Create a new question from the validated data"""

        # topic_name = validated_data['topic'] if 'topic' in validated_data else None
        # topic_id = validated_data['topic_id'] if 'topic_id' in validated_data else None
        subtopic_name = validated_data['subtopic'] if 'subtopic' in validated_data else None
        subtopic_id = validated_data['subtopic_id'] if 'subtopic_id' in validated_data else None
        user_id = validated_data['user_id']

        filter_dict = {}
        subtopic = None
        topic = None

        if subtopic_id is not None:
            filter_dict['id'] = subtopic_id
        if subtopic_name is not None:
            filter_dict['name'] = subtopic_name
        if filter_dict != {}:
            subtopic = Subtopic.objects.filter(**filter_dict)[0] \
                if Subtopic.objects.filter(**filter_dict).count() > 0 else None

            filter_dict = {'name': subtopic.topic.name}
            if Topic.objects.filter(**filter_dict).count() > 0:
                topic = Topic.objects.filter(**filter_dict)[0]
            else:
                raise ValueError("The topic of this subtopic does not exist.")

        if subtopic is None:
            raise ValueError("The subtopic is not defined.")

        # Create questions
        question = Question.objects.get_or_create(
            user_profile_id=user_id,
            topic=topic,
            subtopic=subtopic,
            question=validated_data['question'],
            correctAnswers=validated_data['correctAnswers'],
            difficulty=validated_data['set_difficulty'],
            set_difficulty=validated_data['set_difficulty'],
        )[0]

        dependencies = validated_data['dependencies'] if 'dependencies' in validated_data else None
        dependencies_id = validated_data['dependencies_id'] if 'dependencies_id' in validated_data else None
        validation_type = validated_data['validation_type'] if 'validation_type' in validated_data else None
        appendix = validated_data['appendix'] if 'appendix' in validated_data else None
        hint = validated_data['hint'] if 'hint' in validated_data else None
        imageSrc = validated_data['imageSrc'] if 'imageSrc' in validated_data else None

        if dependencies is not None and dependencies != "":
            dependencies_string = dependencies.split(';')
            for dependency_string in dependencies_string:
                filter_dict = {'name': dependency_string}
                try:
                    dependency = Subtopic.objects.filter(**filter_dict)[0]
                    question.dependencies.add(dependency)
                except:
                    pass

        if dependencies_id is not None and dependencies_id != "":
            dependencies_string = dependencies_id.split(';')
            for dependency_string in dependencies_string:
                filter_dict = {'id': dependency_string}
                try:
                    dependency = Subtopic.objects.filter(**filter_dict)[0]
                    question.dependencies.add(dependency)
                except:
                    pass

        if validation_type is not None and validation_type != '':
            question.validation_type = validation_type
        if appendix is not None and appendix != '':
            question.appendix = appendix
        if hint is not None and hint != '':
            question.hint = hint
        if imageSrc is not None and imageSrc != '':
            question.imageSrc = imageSrc

        return question


class QuestionSerializer(serializers.ModelSerializer):
    """Serializes questions"""

    class Meta:
        model = Question
        fields = ('id', 'created_on', 'topic', 'subtopic', 'dependencies',
                  'question', 'correctAnswers', 'appendix', 'hint', 'imageSrc',
                  'user_profile', 'validation_type', 'difficulty', 'set_difficulty')
        extra_kwargs = {'user_profile': {'read_only': True}, 'appendix': {'required': False}}
