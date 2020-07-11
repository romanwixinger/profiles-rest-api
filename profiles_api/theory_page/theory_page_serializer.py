from rest_framework import serializers

from profiles_api.models import UserProfile
from profiles_api.theory_page.theory_page_model import TheoryPage
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.test.test_model import Test


class TheoryPageDeserializer(serializers.Serializer):
    """Deserializes theory pages"""

    subtopic = serializers.CharField(max_length=255, required=False, allow_blank=False)
    subtopic_id = serializers.IntegerField(required=False, allow_null=False)
    title = serializers.CharField(max_length=255, required=True, allow_blank=False)
    html = serializers.CharField(max_length=1024, required=False, allow_blank=False)
    test = serializers.CharField(max_length=255, required=False, allow_blank=False)
    test_id = serializers.IntegerField(required=False, allow_null=False)

    def validate(self, data):
        """Validate theory page"""

        if 'subtopic' not in data and 'subtopic_id' not in data:
            serializers.ValidationError("Subtopic is not defined.")

        if 'title' not in data or data['title'] == '':
            serializers.ValidationError("Title is invalid or not defined.")

        return data

    def create(self, validated_data):
        """Create a theory page"""

        user_id = validated_data['user_id']
        filter_dict = {'id': user_id}
        user = UserProfile.objects.filter(**filter_dict)[0]

        if 'subtopic_id' in validated_data:
            filter_dict = {'id': validated_data['subtopic_id']}
            subtopic = Subtopic.objects.filter(**filter_dict)[0] if Subtopic.objects.filter(**filter_dict).count() > 0 else None
        else:
            filter_dict = {'name': validated_data['subtopic']}
            subtopic = Subtopic.objects.filter(**filter_dict)[0] if Subtopic.objects.filter(**filter_dict).count() > 0 else None
        if subtopic is None:
            raise ValueError("The subtopic does not exist.")

        topic = subtopic.topic
        html = validated_data['html'] if 'html' in validated_data else ""

        if 'test_id' in validated_data:
            filter_dict = {'id': validated_data['test_id']}
            test = Test.objects.filter(**filter_dict)[0] if Test.objects.filter(**filter_dict).count() > 0 else None
        else:
            filter_dict = {'title': validated_data['test']}
            test = Test.objects.filter(**filter_dict)[0] if Test.objects.filter(**filter_dict).count() > 0 else None

        if test is None:
            raise ValueError("The test does not exist.")

        theory_page = TheoryPage(
            user_profile=user,
            topic=topic,
            subtopic=subtopic,
            title=validated_data['title'],
            html=html,
            test=test
        )
        theory_page.save()

        return theory_page


class TheoryPageSerializer(serializers.ModelSerializer):
    """Serializes theory page"""

    class Meta:
        model = TheoryPage
        fields = ('id', 'user_profile', 'created_on', 'updated_on', 'topic', 'subtopic', 'title', 'html', 'test')
        extra_kwargs = {'user_profile': {'read_only': True}}
