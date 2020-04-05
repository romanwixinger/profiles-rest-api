from rest_framework import serializers

from profiles_api.test.test_model import Test


class TestSerializer(serializers.ModelSerializer):
    """Serializes tests"""

    class Meta:
        model = Test
        fields = ('id', 'user_profile', 'questions', 'title', 'html', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}
