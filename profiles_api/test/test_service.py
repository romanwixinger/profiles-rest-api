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

    @classmethod
    def get_tests(cls, query_params_dict: dict) -> list:
        """Get tests according to query parameters stored in a dict"""

        test_id = query_params_dict['id'] if 'id' in query_params_dict else None
        title = query_params_dict['title'] if 'title' in query_params_dict else None

        filter_dict = {}
        if test_id is not None and test_id.isdigit():
            print("true")
            filter_dict['id'] = int(test_id)
        if title is not None:
            filter_dict['title'] = title

        tests = Test.objects.filter(**filter_dict)

        start = query_params_dict['start'] if 'start' in query_params_dict else None
        number = query_params_dict['number'] if 'number' in query_params_dict else None

        if start is not None:
            tests = tests[min(abs(int(start)), tests.count()):]
        if number is not None:
            tests = tests[:max(0, min(int(number), tests.count()))]

        return tests

