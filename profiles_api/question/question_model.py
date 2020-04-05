from django.db import models
from django.conf import settings

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
    validation = models.CharField(max_length=255, blank=True)
    appendix = models.CharField(max_length=1024, blank=True)
    hint = models.CharField(max_length=1024, blank=True)
    imageSrc = models.CharField(max_length=1024, blank=True)

    def __str__(self):
        """Return the model as a string"""
        return self.question
