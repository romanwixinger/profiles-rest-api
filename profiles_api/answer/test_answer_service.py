from django.test import TestCase

from profiles_api.answer.answer_model import Answer
from profiles_api.answer.answer_service import AnswerService
from profiles_api.models import UserProfile
from profiles_api.question.question_model import Question
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.topic.topic_model import Topic


class TestAnswerService(TestCase):

    def setUp(self):
        user = UserProfile.objects.create(username="unittest", name="unittest")
        topic = Topic.objects.create(user_profile=user, name="unittest")
        subtopic = Subtopic.objects.create(user_profile=user, topic=topic, name="unittest", html="unittest")
        question = Question.objects.create(user_profile=user, topic=topic, subtopic=subtopic, question="unittest",
                                           correctAnswers="unittest")
        self.answer = Answer.objects.create(user_profile=user, question=question, duration=float("5.5"))

    def test_perform_correction_answer_none(self):
        self.answer.answers = None
        self.answer.question.validation_type = 'anything'

        corrected_answer = AnswerService.perform_correction(self.answer)
        self.assertFalse(corrected_answer.correct)

    def test_perform_correction_std_validation_valid(self):
        self.answer.answers = 'correct_unit_test_answer'
        self.answer.question.correctAnswers = 'correct_unit_test_answer'
        self.answer.question.validation_type = None

        corrected_answer = AnswerService.perform_correction(self.answer)
        self.assertTrue(corrected_answer.correct)

    def test_perform_correction_std_validation_not_valid(self):
        self.answer.answers = 'incorrect_unit_test_answer'
        self.answer.question.correctAnswers = 'correct_unit_test_answer'
        self.answer.question.validation_type = None

        corrected_answer = AnswerService.perform_correction(self.answer)
        self.assertFalse(corrected_answer.correct)
