from django.db import models
from django.conf import settings
from django.utils.timezone import utc

import datetime
import numpy as np

from profiles_api.topic.topic_model import Topic
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.utils.utils_service import UtilsService


class Question(models.Model):
    """Question"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    subtopic = models.ForeignKey(Subtopic, related_name='question_subtopic', on_delete=models.CASCADE)
    dependencies = models.ManyToManyField(Subtopic, related_name='question_dependencies', blank=True)
    question = models.CharField(max_length=1024)
    correctAnswers = models.CharField(max_length=1024)
    validation_type = models.CharField(max_length=255, choices=[('standardValidation', ''),
                                                                ('multipleStrings', 'multipleStrings'),
                                                                ('singleFraction', 'singleFraction')])
    appendix = models.CharField(max_length=1024, blank=True)
    hint = models.CharField(max_length=1024, blank=True)
    imageSrc = models.CharField(max_length=1024, blank=True)
    # Manually set difficulty
    set_difficulty = models.IntegerField(blank=False, default=0)

    # Percentage of correct answers
    facility = models.FloatField(blank=False, default=0.5)
    facility_updated_on = models.DateTimeField(auto_now_add=True)
    number_of_answers = models.IntegerField(blank=False, default=0)

    # Difficulty estimated over facility and set difficulty
    difficulty = models.IntegerField(blank=False, default=3)
    difficulty_updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.question

    def time_diff_facility(self):
        """Return the time [s] passed since the last update of the facility"""
        if self.facility_updated_on:
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            return (now - self.facility_updated_on).total_seconds()
        else:
            return 10**6

    def time_diff_difficulty(self):
        """Return the time [s] passed since the last update of the difficulty"""
        if self.difficulty_updated_on:
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            return (now - self.difficulty_updated_on).total_seconds()
        else:
            return 10**6

    @classmethod
    def search_questions(cls, query_params_dict: dict) -> list:
        """Get questions according to query parameters stored in a dict"""

        filter_args = {'question': 'question', 'topic': 'topic_name', 'topic_id': 'topic__id',
                       'difficulty': 'difficulty', 'subtopic': 'subtopic__name', 'subtopic_id': 'subtopic'}

        filter_dict = {filter_args[key]: query_params_dict[key] for key in filter_args.keys()
                       if key in query_params_dict}

        questions = list(Question.objects.filter(**filter_dict))
        questions = UtilsService.select_items(questions, query_params_dict)

        return questions

    @classmethod
    def get_questions(cls, question_id_list: [int]) -> list:
        """Returns a list with the requested questions"""

        questions = cls.objects.filter(id__in=question_id_list)
        question_list = list(questions)

        return question_list

    @classmethod
    def questions_of_level(cls, subtopic_id: int, difficulty: int, number: int = -1) -> [int]:
        """Get a number of question ids of a subtopic of a certain level of difficulty"""

        filter_dict = {'subtopic__id': subtopic_id, 'difficulty': difficulty}
        questions = Question.objects.filter(**filter_dict).values_list('id', flat=True)

        question_list = list(questions)

        if number == -1:
            return question_list

        return question_list[:max(0, min(int(number), questions.count()))]

    @classmethod
    def update_facility(cls, question, correct: bool):
        """Update the facility and number of answers of a certain question"""

        correct_answers = question.facility * question.number_of_answers + int(correct)
        question.number_of_answers += 1

        question.facility = correct_answers / question.number_of_answers
        question.facility_updated_on.now()

        question.save()

        return

    @classmethod
    def update_difficulty(cls, subtopic: Subtopic, new_answer: bool=True, force_update: bool=False):
        """Update the difficulties of all question of a certain subtopic"""

        subtopic.answers_since_update += int(new_answer)
        subtopic.save()
        if subtopic.answers_since_update < 20 and not force_update:
            return
        else:
            subtopic.answers_since_update = 0
            subtopic.save()

        questions = np.array(list(Question.objects.filter(subtopic=subtopic)))
        facilities = np.array([question.facility for question in questions])
        set_difficulties = np.array([question.set_difficulty for question in questions])

        # Separate calculation
        fac_difficulty = 6 - 5*facilities
        difficulties = 0.7 * set_difficulties + 0.3 * fac_difficulty

        # Normalisation of difficulties so that std = 1 and mean = 3
        difficulties = (difficulties + 3 - np.mean(difficulties)) / np.std(difficulties) if np.std(difficulties) > 0 else difficulties

        # Norm to integers
        for i, question in enumerate(questions):
            question.difficulty = max(1, min(difficulties[i] + 0.5, 5))
            question.difficulty_updated_on.now()
            question.save()

        return
