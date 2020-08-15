from rest_framework import serializers

from profiles_api.test.test_model import Test


class TestDeserializer(serializers.Serializer):
    """Deserializes tests"""

    questions = serializers.CharField(max_length=1024, required=True)
    title = serializers.CharField(max_length=255, required=True)
    html = serializers.CharField(max_length=8191, required=False)

    def validate(self, data):
        """Validate the data"""

        if 'questions' not in data or data['questions'] == '':
            raise serializers.ValidationError("No questions provided.")

        question_list = data['questions'].split(';')

        for question_str in question_list:
            if not question_str.isdigit():
                raise serializers.ValidationError("Invalid question Ids provided.")

        return data

    def create(self, validated_data):
        """Create a new test"""

        user_id = validated_data['user_id']
        html = validated_data['html'] if 'html' in validated_data else ""
        title = validated_data['title']
        question_id_list = [int(question_id) for question_id in validated_data['questions'].split(';')]

        test = Test.create_test(user_id=user_id,
                                question_id_list=question_id_list,
                                title=title,
                                html=html,
                                creation_type="standard")
        return test


class TestSerializer(serializers.ModelSerializer):
    """Serializes tests"""

    class Meta:
        model = Test
        fields = ('id', 'user_profile', 'questions', 'title', 'html', 'created_on', 'creation_type')
        extra_kwargs = {'user_profile': {'read_only': True}}


