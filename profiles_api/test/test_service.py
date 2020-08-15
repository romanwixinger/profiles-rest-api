from profiles_api.models import UserProfile
from profiles_api.test.test_model import Test
from profiles_api.subtopic.subtopic_model import Subtopic
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
        solved_tests = Test.solved_tests(user.id)

        for test_id in solved_tests:
            if test_id in recommended_tests:
                recommended_tests.remove(test_id)
                recommended_tests = [test_id] + recommended_tests

        return recommended_tests[-number:]

    @classmethod
    def get_recommended_tests(cls, user: UserProfile, number: int = 2) -> [Test]:
        """"Evaluates all completed tests of the user and recommends tests accordingly"""

        test_id_list = cls.recommended_tests(user=user, number=number)
        recommended_tests = Test.get_tests(test_id_list=test_id_list)

        return recommended_tests

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
    def create_recommended_test(cls, user: UserProfile, number: int, length: int, title: str, html: str = "") -> Test:
        """Create a test of recommended questions of number-many subtopics.
        For each subtopic there are at most length-many questions"""

        recommended_questions = QuestionService.recommended_questions(user=user, number=number, length=length)

        test = Test.create_test(user_id=user.id, question_id_list=recommended_questions, title=title, html=html)
        return test

    @classmethod
    def subtopic_frequency_dict(cls,  question_id_list: [int]) -> dict:
        """Creates a dict with the occurring subtopics as keys and the number of occurrences as value"""

        subtopic_frequency_dict = {}

        question_list = Question.get_questions(question_id_list)
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
