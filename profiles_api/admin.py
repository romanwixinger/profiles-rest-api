from django.contrib import admin

from profiles_api import models

from profiles_api.topic.topic_model import Topic

admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)
admin.site.register(models.Question)
admin.site.register(Topic)
admin.site.register(models.Answer)
admin.site.register(models.Test)
admin.site.register(models.CompletedTest)
admin.site.register(models.TheoryPage)

