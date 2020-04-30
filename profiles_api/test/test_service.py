from profiles_api.models import UserProfile
from profiles_api.test.test_model import Test
from profiles_api.subtopic.subtopic_service import SubtopicService
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.completed_test.completed_test_model import CompletedTest
from profiles_api.question.question_model import Question


class TestService:

    @classmethod
    def recommended_tests(cls, user: UserProfile, number: int = 2) -> [int]:
        """"Evaluates all completed tests of the user and recommends test ids accordingly"""

        recommended_subtopics = SubtopicService.recommended_subtopics(user)
        if recommended_subtopics is None or len(recommended_subtopics) == 0:
            return []

        test_accordance_dict = cls.test_accordance_dict(recommended_subtopics)

        recommended_tests = [test for _, test in sorted(zip(test_accordance_dict.values(), test_accordance_dict.keys()))]

        # Solved tests are avoided in the recommendation.
        solved_tests = cls.solved_tests(user.id)

        for test_id in solved_tests:
            if test_id in recommended_tests:
                recommended_tests.remove(test_id)
                recommended_tests = [test_id] + recommended_tests

        return recommended_tests[-number:]

    @classmethod
    def get_recommended_tests(cls, user: UserProfile, number: int = 2) -> [Test]:
        """"Evaluates all completed tests of the user and recommends tests accordingly"""

        test_id_list = cls.recommended_tests(user=user, number=number)
        recommended_tests = cls.get_tests(test_id_list=test_id_list)

        return recommended_tests

    @classmethod
    def get_tests(cls, test_id_list: [int]) -> [Test]:
        """Gets specific tests"""

        tests = []

        for test_id in test_id_list:
            filter_dict = {'id': test_id}
            test = Test.objects.get(**filter_dict)[0] if Test.objects.get(**filter_dict).count() > 0 else None
            if test is None:
                raise LookupError
            else:
                tests.append(test)

        return tests

    @classmethod
    def search_tests(cls, query_params_dict: dict) -> list:
        """Get tests according to query parameters stored in a dict"""

        test_id = query_params_dict['id'] if 'id' in query_params_dict else None
        title = query_params_dict['title'] if 'title' in query_params_dict else None

        filter_dict = {}
        if test_id is not None and ((test_id is str and test_id.isdigit()) or test_id is int):
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

    @classmethod
    def solved_tests(cls, user_id) -> [int]:
        """Get a list with the ids of all the tests that have been solved"""

        filter_dict = {'user_profile': user_id}
        completed_tests = CompletedTest.objects.filter(**filter_dict)
        solved_tests = [completed_test.test.id for completed_test in completed_tests]

        unique_solved_tests = {}
        for solved_test in solved_tests:
            unique_solved_tests[solved_test] = 1

        return list(unique_solved_tests.keys())

    @classmethod
    def create_test(cls, user_id: int, question_id_list: [int], title: str, html: str = "") -> Test:
        """Create a test"""

        filter_dict = {'id': user_id}
        user = UserProfile.objects.filter(**filter_dict)[0]

        test = Test.objects.create(
            user_profile=user,
            title=title,
            html=html,

        )

        test.save()

        for question_id in question_id_list:
            filter_dict = {'id': question_id}
            question = Question.objects.filter(**filter_dict)[0]\
                if Question.objects.filter(**filter_dict).count() > 0 else None
            if question is None:
                raise LookupError
            else:
                test.questions.add(question)

        return test
