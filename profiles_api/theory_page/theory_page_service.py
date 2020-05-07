import random

from profiles_api.models import UserProfile
from profiles_api.theory_page.theory_page_model import TheoryPage
from profiles_api.subtopic.subtopic_service import SubtopicService


class TheoryPageService:

    @classmethod
    def recommended_theory_pages(cls, user: UserProfile, number: int = 2) -> [int]:
        """"Evaluates all completed tests of the user and recommends theory pages accordingly"""

        recommended_subtopics = SubtopicService.recommended_subtopics(user, number=10*number)
        if recommended_subtopics is None:
            return []

        recommended_theory_pages = []  # contains ids
        for recommended_subtopic in recommended_subtopics:
            filter_dict = {'subtopic': recommended_subtopic}
            theory_pages = TheoryPage.objects.filter(**filter_dict)
            if theory_pages is None:
                continue
            for theory_page in theory_pages:
                recommended_theory_pages.append(theory_page.id)
            if len(recommended_theory_pages) >= number:
                break

        return recommended_theory_pages[:number]

    @classmethod
    def search_theory_pages(cls, query_params_dict: dict) -> [TheoryPage]:
        """Get theory pages according to query parameters stored in a dict"""

        theory_page_id = query_params_dict['id'] if 'id' in query_params_dict else None
        title = query_params_dict['title'] if 'title' in query_params_dict else None

        filter_dict = {}
        if theory_page_id is not None and theory_page_id.isdigit():
            filter_dict['id'] = int(theory_page_id)
        if title is not None:
            filter_dict['title'] = title

        theory_pages = list(TheoryPage.objects.filter(**filter_dict))

        start = query_params_dict['start'] if 'start' in query_params_dict else None
        number = query_params_dict['number'] if 'number' in query_params_dict else None
        mode = query_params_dict['mode'] if 'mode' in query_params_dict else None

        if mode == 'random':
            random.shuffle(theory_pages)
        if start is not None:
            theory_pages = theory_pages[min(abs(int(start)), len(theory_pages)):]
        if number is not None:
            theory_pages = theory_pages[:max(0, min(int(number), len(theory_pages)))]

        return theory_pages

    @classmethod
    def get_theory_pages(cls, theory_page_id_list: [int]) -> [TheoryPage]:
        """Returns a list with the requested theory_pages"""

        theory_pages = TheoryPage.objects.filter(id__in=theory_page_id_list)
        theory_pages_list = list(theory_pages)

        return theory_pages_list
