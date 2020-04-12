from django.db import models
from django.conf import settings


class Topic(models.Model):
    """Topic"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        """Return the model as a string"""
        return self.name
