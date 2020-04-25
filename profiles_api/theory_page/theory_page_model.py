from django.db import models
from django.conf import settings

from profiles_api.topic.topic_model import Topic
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.test.test_model import Test


class TheoryPage(models.Model):
    """Theory page"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=255)
    html = models.CharField(max_length=8191, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        """Return the model as a string"""
        return self.title

