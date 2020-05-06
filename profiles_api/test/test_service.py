import random

from profiles_api.models import UserProfile
from profiles_api.test.test_model import Test
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.completed_test.completed_test_model import CompletedTest
from profiles_api.question.question_model import Question

from profiles_api.subtopic.subtopic_service import SubtopicService
from profiles_api.question.question_service import QuestionService


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
        start = query_params_dict['start'] if 'start' in query_params_dict else None
        number = query_params_dict['number'] if 'number' in query_params_dict else None
        mode = query_params_dict['mode'] if 'mode' in query_params_dict else None

        filter_dict = {}
        if test_id is not None and ((test_id is str and test_id.isdigit()) or test_id is int):
            filter_dict['id'] = int(test_id)
        if title is not None:
            filter_dict['title'] = title

        tests = list(Test.objects.filter(**filter_dict))

        if mode == 'random':
            random.shuffle(tests)
        if start is not None:
            tests = tests[min(abs(int(start)), len(tests)):]
        if number is not None:
            tests = tests[:max(0, min(int(number), len(tests)))]

        return tests

    @classmethod
    def test_accordance_dict(cls, recommended_subtopics: [Subtopic]):
        """Get a dict with test ids as keys and their accordance with the recommended subtopics as value"""

        test_accordance_dict = {}

        tests = Test.objects.all()
        for test in tests:
            question_id_list = [question.id for question in test.questions.all()]
            subtopic_frequency_dict = cls.subtopic_frequency_dict(question_id_list)
            test_accordance_dict[test.id] = cls.accordance(recommended_subtopics, subtopic_frequency_dict)

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

        test.save()

        return test

    @classmethod
    def create_recommended_test(cls, user: UserProfile, number: int, length: int, title: str, html: str = "") -> Test:
        """Create a test of recommended questions of number-many subtopics.
        For each subtopic there are at most length-many questions"""

        recommended_questions = QuestionService.recommended_questions(user=user, number=number, length=length)

        test = cls.create_test(user_id=user.id, question_id_list=recommended_questions, title=title, html=html)
        return test

    @classmethod
    def subtopic_frequency_dict(cls,  question_id_list: [int]) -> dict:
        """Creates a dict with the occurring subtopics as keys and the number of occurrences as value"""

        subtopic_frequency_dict = {}

        question_list = QuestionService.get_questions(question_id_list)
        for question in question_list:
            if question.subtopic.id in subtopic_frequency_dict:
                subtopic_frequency_dict[question.subtopic.id] += 1
            else:
                subtopic_frequency_dict[question.subtopic.id] = 1

            dependencies = question.dependencies.all() if question.dependencies is not None else []
            for dependency in dependencies:
                if dependency.id in subtopic_frequency_dict:
                    subtopic_frequency_dict[dependency.id] += 1
                else:
                    subtopic_frequency_dict[dependency.id] = 1

        return subtopic_frequency_dict

    @classmethod
    def accordance(cls, recommended_subtopics: [int], subtopic_frequency_dict: dict) -> float:
        """Quantifies the accordance between a list of recommended subtopics and test"""

        if len(recommended_subtopics) == 0 or subtopic_frequency_dict == {}:
            return 0

        accordance = 0
        for subtopic_id in recommended_subtopics:
            accordance += subtopic_frequency_dict[subtopic_id] if subtopic_id in subtopic_frequency_dict else 0

        accordance /= len(subtopic_frequency_dict.keys())
        return accordance
