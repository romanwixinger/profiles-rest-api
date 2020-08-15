from profiles_api.models import UserProfile
from profiles_api.theory_page.theory_page_model import TheoryPage

from profiles_api.subtopic.subtopic_service import SubtopicService


class TheoryPageService:

    @classmethod
    def recommended_theory_pages(cls, user: UserProfile, number: int = 2) -> [int]:
        """"Evaluates all completed tests of the user and recommends theory pages accordingly"""

        recommended_subtopics = SubtopicService.recommended_subtopics(user)
        if recommended_subtopics is None:
            return []

        recommended_theory_pages = TheoryPage.search_theory_pages_with_subtopic(subtopic_id_list=recommended_subtopics,
                                                                         number=number)
        return recommended_theory_pages


