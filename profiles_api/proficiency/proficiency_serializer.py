from rest_framework import serializers

from profiles_api.proficiency.proficiency_model import Proficiency


class ProficiencySerializer(serializers.ModelSerializer):
    """Serializes the proficiency"""

    class Meta:
        model = Proficiency
        fields = ('id', 'user_profile', 'subtopic', 'level', 'updated_on')
        extra_kwargs = {'user_profile': {'read_only': True}}
