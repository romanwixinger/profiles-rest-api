from django.db import models
from django.conf import settings

from profiles_api.question.question_model import Question


class Test(models.Model):
    """Generic test"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    questions = models.ManyToManyField(Question)
    title = models.CharField(max_length=255)
    html = models.CharField(max_length=1024, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.title

