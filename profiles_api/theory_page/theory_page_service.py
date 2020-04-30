from profiles_api.models import UserProfile
from profiles_api.theory_page.theory_page_model import TheoryPage
from profiles_api.subtopic.subtopic_service import SubtopicService


class TheoryPageService:

    @classmethod
    def recommended_theory_pages(cls, user: UserProfile, number: int = 2) -> [int]:
        """"Evaluates all completed tests of the user and recommends theory pages accordingly"""

        recommended_subtopics = SubtopicService.recommended_subtopics(user, number)
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

        theory_pages = TheoryPage.objects.filter(**filter_dict)

        start = query_params_dict['start'] if 'start' in query_params_dict else None
        number = query_params_dict['number'] if 'number' in query_params_dict else None

        if start is not None:
            theory_pages = theory_pages[min(abs(int(start)), theory_pages.count()):]
        if number is not None:
            theory_pages = theory_pages[:max(0, min(int(number), theory_pages.count()))]

        return theory_pages



