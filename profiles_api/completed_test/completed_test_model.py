from django.db import models
from django.conf import settings

from profiles_api.answer.answer_model import Answer
from profiles_api.subtopic.subtopic_model import Subtopic


class CompletedTest(models.Model):
    """Completed test"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    answers = models.ManyToManyField(Answer, blank=True)
    state = models.CharField(max_length=255, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    duration = models.DecimalField(max_digits=8, decimal_places=2, blank=True)  # in seconds
    comment = models.CharField(max_length=1024, blank=True)
    recommendedSubtopics = models.ManyToManyField(Subtopic, blank=True)

    def __str__(self):
        """Return the model as a string"""
        return "Test started on " + self.created_on.__str__() + "."

    
