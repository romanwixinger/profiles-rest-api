from profiles_api.models import UserProfile
from profiles_api.test.test_model import Test
from profiles_api.subtopic.subtopic_service import SubtopicService


class TestService:

    @classmethod
    def get_recommended_tests(cls, user: UserProfile, number: int = 2) -> list:
        """"Evaluates all completed tests of the user and recommends tests accordingly"""

        recommended_subtopics = SubtopicService.get_recommended_subtopics(user)
        if recommended_subtopics is None or len(recommended_subtopics) == 0:
            return []

        recommended_tests = []  # contains ids
        for recommended_subtopic in recommended_subtopics:
            filter_dict = {'questions__subtopic_id': int(recommended_subtopic)}
            tests = Test.objects.filter(**filter_dict)
            if tests is None:
                continue
            for test in tests:
                recommended_tests.append(test.id)

        return recommended_tests[:number]

