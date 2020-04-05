from rest_framework import serializers

from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}


class AnswerSerializer(serializers.ModelSerializer):
    """Serializes answers"""

    class Meta:
        model = models.Answer
        fields = ('id', 'user_profile', 'created_on', 'question',
                  'duration', 'answers', 'correct', 'skipped', 'comment')
        extra_kwargs = {'user_profile': {'read_only': True}}


class TestSerializer(serializers.ModelSerializer):
    """Serializes tests"""

    class Meta:
        model = models.Test
        fields = ('id', 'user_profile', 'questions', 'title', 'html', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}


class CompletedTestSerializer(serializers.ModelSerializer):
    """Serializes completed tests"""

    class Meta:
        model = models.CompletedTest
        fields = ('id', 'user_profile', 'answers', 'state', 'created_on',
                  'updated_on', 'duration', 'comment', 'recommendedSubtopics')
        extra_kwargs = {'user_profile': {'read_only': True}}


class TheoryPageSerializer(serializers.ModelSerializer):
    """Serializes theory page"""

    class Meta:
        model = models.TheoryPage
        fields = ('id', 'user_profile', 'created_on', 'updated_on', 'topic', 'subtopic', 'title', 'html', 'test')
        extra_kwargs = {'user_profile': {'read_only': True}}

