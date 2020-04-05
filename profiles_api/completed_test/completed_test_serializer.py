from rest_framework import serializers

from profiles_api.completed_test.completed_test_model import CompletedTest


class CompletedTestSerializer(serializers.ModelSerializer):
    """Serializes completed tests"""

    class Meta:
        model = CompletedTest
        fields = ('id', 'user_profile', 'answers', 'state', 'created_on',
                  'updated_on', 'duration', 'comment', 'recommendedSubtopics')
        extra_kwargs = {'user_profile': {'read_only': True}}
