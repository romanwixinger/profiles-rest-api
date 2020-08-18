from django.db import models
from django.conf import settings

from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.question.question_model import Question

from profiles_api.utils.utils_service import UtilsService


class Proficiency(models.Model):
    """Proficiency of a user in a certain subtopic"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, blank=False)
    level = models.IntegerField(blank=False, default=1)
    answers_since_update = models.IntegerField(blank=False, default=0)
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

        proficiencies = cls.objects.filter(**query_dict)
        proficiencies = UtilsService.select_items(items=list(proficiencies), query_params_dict=query_params_dict)

        return proficiencies

    @classmethod
    def difficulty_list(cls, question_id_list: [int]) -> [int]:
        """Takes a list of question ids and return a list of their difficulties"""

        difficulty_list = []

        for question_id in question_id_list:
            question = Question.objects.get(pk=question_id)
            difficulty_list.append(question.difficulty)

        return difficulty_list

    @classmethod
    def proficiency_level(cls, user_id: int, subtopic_id: int):
        """Get the level of a user in a specific subtopic. The knowledge level takes values between 1 to 5
        where 5 is the best level. If the user did not give any answers in this subtopic, the level is 0."""

        proficiencies = Proficiency.search_proficiencies(query_params_dict={'user_profile': user_id,
                                                                            'subtopic_id': subtopic_id})
        if len(proficiencies) == 1:
            return proficiencies[0].level
        else:
            return 0

    @classmethod
    def proficiency_list(cls, user_id: int, subtopic_id_list: [int]) -> dict:
        """Get the knowledge level of a user for a list of subtopics"""

        level_dict = {}

        for subtopic_id in subtopic_id_list:
            level_dict[subtopic_id] = Proficiency.proficiency_level(user_id=user_id, subtopic_id=subtopic_id)

        return level_dict



