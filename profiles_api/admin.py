from django.contrib import admin

from profiles_api import models

from profiles_api.topic.topic_model import Topic
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.question.question_model import Question
from profiles_api.answer.answer_model import Answer
from profiles_api.test.test_model import Test


admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)
admin.site.register(Question)
admin.site.register(Topic)
admin.site.register(Subtopic)
admin.site.register(Answer)
admin.site.register(Test)
admin.site.register(models.CompletedTest)
admin.site.register(models.TheoryPage)

