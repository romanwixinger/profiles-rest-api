from profiles_api.models import UserProfile

from profiles_api.topic.topic_service import TopicService
from profiles_api.theory_page.theory_page_model import TheoryPage
from profiles_api.subtopic.subtopic_service import SubtopicService


class TheoryPageService:

    @classmethod
    def recommended_theory_pages(cls, user: UserProfile, number: int = 2) -> [int]:
        """"Evaluates all completed tests of the user and recommends theory pages accordingly"""

        recommended_subtopics = SubtopicService.recommended_subtopics(user)
        if recommended_subtopics is None:
            return []

        recommended_theory_pages = cls.search_theory_pages_with_subtopic(subtopic_id_list=recommended_subtopics,
                                                                         number=number)
        return recommended_theory_pages

    @classmethod
    def search_theory_pages(cls, query_params_dict: dict) -> [TheoryPage]:
        """Get theory pages according to query parameters stored in a dict"""

        filter_dict = {}
        if 'id' in query_params_dict and query_params_dict['id'].isdigit():
            filter_dict['id'] = int(query_params_dict['id'])
        if 'title' in query_params_dict:
            filter_dict['title'] = query_params_dict['title']

        theory_pages = list(TheoryPage.objects.filter(**filter_dict))
        theory_pages = TopicService.select_items(items=theory_pages, query_params_dict=query_params_dict)

        return theory_pages

    @classmethod
    def get_theory_pages(cls, theory_page_id_list: [int]) -> [TheoryPage]:
        """Returns a list with the requested theory_pages"""

        theory_pages = TheoryPage.objects.filter(id__in=theory_page_id_list)
        theory_pages_list = list(theory_pages)

        return theory_pages_list

    @classmethod
    def search_theory_pages_with_subtopic(cls, subtopic_id_list: [int], number: int) -> [int]:
        """Retrieve number-many theory pages that cover certain subtopics"""

        theory_page_id_list = []

        for subtopic_id in subtopic_id_list:
            filter_dict = {'subtopic': subtopic_id}
            theory_pages = TheoryPage.objects.filter(**filter_dict)
            if theory_pages is None:
                continue
            for theory_page in theory_pages:
                theory_page_id_list.append(theory_page.id)
            if len(theory_page_id_list) >= number:
                break

        return theory_page_id_list[:number]
