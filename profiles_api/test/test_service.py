from profiles_api.models import UserProfile
from profiles_api.test.test_model import Test
from profiles_api.subtopic.subtopic_service import SubtopicService
from profiles_api.subtopic.subtopic_model import Subtopic


class TestService:

    @classmethod
    def get_recommended_tests(cls, user: UserProfile, number: int = 2) -> list:
        """"Evaluates all completed tests of the user and recommends tests accordingly"""

        recommended_subtopics = SubtopicService.get_recommended_subtopics(user)
        if recommended_subtopics is None or len(recommended_subtopics) == 0:
            return []

        test_accordance_dict = cls.test_accordance_dict(recommended_subtopics)

        recommended_tests = [test for _, test in sorted(zip(test_accordance_dict.values(), test_accordance_dict.keys()))]

        print(recommended_tests)

        return recommended_tests[-number:]


    @classmethod
    def get_tests(cls, query_params_dict: dict) -> list:
        """Get tests according to query parameters stored in a dict"""

        test_id = query_params_dict['id'] if 'id' in query_params_dict else None
        title = query_params_dict['title'] if 'title' in query_params_dict else None

        filter_dict = {}
        if test_id is not None and test_id.isdigit():
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

    @classmethod
    def test_accordance_dict(cls, recommended_subtopics: [Subtopic]):
        """Get a dict with test ids as keys and their accordance with the recommended subtopics as value"""

        test_accordance_dict = {}

        tests = Test.objects.all()
        for test in tests:
            question_id_list = [question.id for question in test.questions.all()]
            subtopic_frequency_dict = SubtopicService.subtopic_frequency_dict(question_id_list)
            test_accordance_dict[test.id] = SubtopicService.accordance(recommended_subtopics, subtopic_frequency_dict)

        return test_accordance_dict
