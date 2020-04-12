from rest_framework import serializers

from profiles_api.models import UserProfile
from profiles_api.theory_page.theory_page_model import TheoryPage
from profiles_api.topic.topic_model import Topic
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.test.test_model import Test


class TheoryPageDeserializer(serializers.Serializer):
    """Deserializes theory pages"""

    topic = serializers.CharField(max_length=255, required=False)
    topic_id = serializers.IntegerField(required=False)
    subtopic = serializers.CharField(max_length=255, required=False)
    subtopic_id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=255, required=True)
    html = serializers.CharField(max_length=1024, required=False)
    test = serializers.CharField(max_length=255, required=False)
    test_id = serializers.IntegerField(required=False)

    def validate(self, data):
        """Validate theory page"""

        if 'topic' not in data and 'topic_id' not in data:
            serializers.ValidationError("Topic is not defined.")

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

        if 'topic_id' in validated_data:
            filter_dict = {'id': validated_data['topic_id']}
            topic = Topic.objects.filter(**filter_dict)[0]
        else:
            filter_dict = {'name': validated_data['topic']}
            topic = Topic.objects.filter(**filter_dict)[0]
        if topic is None:
            return None

        if 'subtopic_id' in validated_data:
            filter_dict = {'id': validated_data['subtopic_id']}
            subtopic = Subtopic.objects.filter(**filter_dict)[0]
        else:
            filter_dict = {'name': validated_data['subtopic']}
            subtopic = Subtopic.objects.filter(**filter_dict)[0]
        if subtopic is None:
            return None

        html = validated_data['html'] if 'html' in validated_data else ""

        if 'test_id' in validated_data:
            filter_dict = {'id': validated_data['test_id']}
            test = Test.objects.filter(**filter_dict)[0]
        else:
            filter_dict = {'title': validated_data['test']}
            test = Test.objects.filter(**filter_dict)[0]

        if test is None:
            return None

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
