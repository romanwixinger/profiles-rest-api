from django.db import models
from django.conf import settings

from profiles_api.subtopic.subtopic_model import Subtopic

from profiles_api.utils.utils_service import UtilsService


class Proficiency(models.Model):
    """Proficiency of a user in a certain subtopic"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, blank=False)
    level = models.IntegerField(blank=False, default=1)
    number_of_answers = models.IntegerField(blank=False, default=0)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return "The level of " + self.user_profile.name + " in " + self.subtopic.name + " is " + self.level + "."

    @classmethod
    def search_proficiencies(cls, query_params_dict: dict) -> []:
        """Get proficiencies according to query parameters stored in a dict"""

        query_dict = {}

        if 'user_profile' in query_params_dict:
            query_dict['user_profile'] = query_params_dict['user_profile']
        if 'subtopic_id' in query_params_dict:
            query_dict['subtopic'] = query_params_dict['subtopic_id']

        subtopics = cls.objects.filter(**query_dict)
        subtopics = UtilsService.select_items(items=list(subtopics), query_params_dict=query_params_dict)

        return subtopics
