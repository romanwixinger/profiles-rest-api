from django.db import models
from django.conf import settings

from profiles_api.subtopic.subtopic_model import Subtopic


class Proficiency(models.Model):
    """Proficiency of a user in a certain subtopic"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, blank=False)
    level = models.IntegerField(blank=False, default=1)
    number_of_answers = models.IntegerField(blank=False, default=0)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return "The proficiency of " + self.user_profile.name + " in " + self.subtopic.name + " is " + self.level + "."

