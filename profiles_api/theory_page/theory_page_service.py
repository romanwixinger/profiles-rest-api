from profiles_api.models import UserProfile
from profiles_api.theory_page.theory_page_model import TheoryPage
from profiles_api.subtopic.subtopic_service import SubtopicService


class TheoryPageService:

    @classmethod
    def get_recommended_theory_pages(cls, user: UserProfile, number: int = 2) -> list:
        """"Evaluates all completed tests of the user and recommends theory pages accordingly"""

        recommended_subtopics = SubtopicService.get_recommended_subtopics(user, number)
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



