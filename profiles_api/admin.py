from django.contrib import admin

from profiles_api import models

from profiles_api.topic.topic_model import Topic
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.question.question_model import Question
from profiles_api.answer.answer_model import Answer
from profiles_api.test.test_model import Test
from profiles_api.completed_test.completed_test_model import CompletedTest
from profiles_api.theory_page.theory_page_model import TheoryPage
from profiles_api.proficiency.proficiency_model import Proficiency

admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)
admin.site.register(Question)
admin.site.register(Topic)
admin.site.register(Subtopic)
admin.site.register(Answer)
admin.site.register(Test)
admin.site.register(CompletedTest)
admin.site.register(TheoryPage)
admin.site.register(Proficiency)

