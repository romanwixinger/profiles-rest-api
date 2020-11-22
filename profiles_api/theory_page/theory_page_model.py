from django.db import models
from django.conf import settings

from profiles_api.topic.topic_model import Topic
from profiles_api.subtopic.subtopic_model import Subtopic

from profiles_api.utils.utils_service import UtilsService


class TheoryPage(models.Model):
    """Theory page"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=255)
    html = models.CharField(max_length=8191, blank=True)

    def __str__(self):
        """Return the model as a string"""
        return self.title

    @classmethod
    def search_theory_pages(cls, query_params_dict: dict) -> []:
        """Get theory pages according to query parameters stored in a dict"""

        filter_dict = {}
        if 'id' in query_params_dict and query_params_dict['id'].isdigit():
            filter_dict['id'] = int(query_params_dict['id'])
        if 'title' in query_params_dict:
            filter_dict['title'] = query_params_dict['title']

        if 'subtopic_id' in query_params_dict:
            filter_dict['subtopic'] = query_params_dict['subtopic_id']

        theory_pages = list(cls.objects.filter(**filter_dict))
        theory_pages = UtilsService.select_items(items=theory_pages, query_params_dict=query_params_dict)

        return theory_pages

    @classmethod
    def get_theory_pages(cls, theory_page_id_list: [int]) -> []:
        """Returns a list with the requested theory_pages"""

        theory_page_list = UtilsService.get_items(theory_page_id_list, TheoryPage)

        return theory_page_list

    @classmethod
    def search_theory_pages_with_subtopic(cls, subtopic_id_list: [int], number: int) -> [int]:
        """Retrieve number-many theory pages that cover certain subtopics"""

        theory_page_id_list = []

        for subtopic_id in subtopic_id_list:
            filter_dict = {'subtopic': subtopic_id}
            theory_pages = cls.objects.filter(**filter_dict)
            if theory_pages is None:
                continue
            for theory_page in theory_pages:
                theory_page_id_list.append(theory_page.id)
            if len(theory_page_id_list) >= number:
                break

        return theory_page_id_list[:number]
