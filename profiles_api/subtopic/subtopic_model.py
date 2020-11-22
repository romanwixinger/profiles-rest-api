from django.db import models
from django.conf import settings

from profiles_api.topic.topic_model import Topic

from profiles_api.utils.utils_service import UtilsService


class Subtopic(models.Model):
    """Subtopic"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, blank=False)
    html = models.CharField(max_length=8191, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=False)
    # Number of new answers since the difficulty was last updated
    answers_since_update = models.IntegerField(blank=False, default=0)

    def __str__(self):
        """Return the model as a string"""
        return self.name

    @classmethod
    def search_subtopics(cls, query_params_dict: dict) -> []:
        """Get subtopics according to query parameters stored in a dict"""

        if 'topic' in query_params_dict:
            subtopics = cls.objects.filter(**{'topic__name': query_params_dict['topic']})
        elif 'topic_id' in query_params_dict:
            subtopics = cls.objects.filter(**{'topic__id': query_params_dict['topic_id']})
        else:
            subtopics = cls.objects.all()

        subtopics = UtilsService.select_items(items=list(subtopics), query_params_dict=query_params_dict)
        return subtopics

    @classmethod
    def get_subtopics(cls, subtopic_id_list: [int]) -> []:
        """Returns a list with the requested subtopics"""

        subtopics = cls.objects.filter(id__in=subtopic_id_list)
        return list(subtopics)

    @classmethod
    def subtopic_id_list(cls) -> [int]:
        """Get a list with all subtopic ids"""

        return [subtopic.id for subtopic in cls.objects.all()]
