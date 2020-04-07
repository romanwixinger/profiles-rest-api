from rest_framework import serializers

from profiles_api.test.test_model import Test
from profiles_api.question.question_model import Question


class TestDeserializer(serializers.Serializer):
    """Deserializes tests"""

    questions = serializers.charField(max_length=1024)
    title = serializers.charField(max_length=255)
    html = serializers.charField(max_length=1024, required=False)

    def validate(self, data):
        """Validate the data"""

        if 'questions' not in data or data['questions'] == '':
            raise serializers.ValidationError("No questions provided.")

        question_list = data['queestions'].split(';')

        for question_str in question_list:
            if not question_str.isdigit():
                raise serializers.ValidationError("Invalid question Ids provided.")

        return data

    def create(self, validated_data):
        """Create a new test"""

        html = validated_data['html'] if 'html' in validated_data else ""
        test = Test(
            title=validated_data['title'],
            html=html
        )

        question_list = validated_data['questions'].split(';')

        for question_str in question_list:
            filter_dict = {'id': int(question_str)}
            question = Question.objects.filter(**filter_dict)[0]
            if question is None:
                return None
            else:
                test.questions.add(question)

        return question


class TestSerializer(serializers.ModelSerializer):
    """Serializes tests"""

    class Meta:
        model = Test
        fields = ('id', 'user_profile', 'questions', 'title', 'html', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}


