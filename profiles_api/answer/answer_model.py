from django.db import models
from django.conf import settings

from profiles_api.question.question_model import Question


class Answer(models.Model):
    """Answer"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    duration = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=0)  # in seconds
    answers = models.CharField(max_length=1024, blank=True)

    # Fields set after correction
    correct = models.BooleanField(blank=True, default=False)
    skipped = models.BooleanField(blank=True, default=False)
    comment = models.CharField(max_length=1024, blank=True, default="")

    def __str__(self):
        """Return the model as a string"""
        return self.answers





