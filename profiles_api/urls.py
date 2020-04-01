from django.urls import path, include

from rest_framework.routers import DefaultRouter

from profiles_api import views


router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
router.register('profile', views.UserProfileViewSet)
router.register('feed', views.UserProfileFeedViewSet)
router.register('question', views.QuestionViewSet)
router.register('subtopic', views.SubtopicViewSet)
router.register('topic', views.TopicViewSet)
router.register('answer', views.AnswerViewSet)
router.register('test', views.TestViewSet)
router.register('completedTest', views.CompletedTestViewSet)
router.register('theoryPage', views.TheoryPageViewSet)


urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('custom-subtopic/', views.CustomSubtopicView.as_view()),
    path('', include(router.urls))
]
