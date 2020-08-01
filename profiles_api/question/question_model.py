from django.db import models
from django.conf import settings
from django.utils.timezone import utc

import datetime

from profiles_api.topic.topic_model import Topic
from profiles_api.subtopic.subtopic_model import Subtopic


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

