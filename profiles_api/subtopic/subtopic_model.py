from django.db import models
from django.conf import settings

from profiles_api.topic.topic_model import Topic


class Subtopic(models.Model):
    """Subtopic"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    html = models.CharField(max_length=1024, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        """Return the model as a string"""
        return self.name


