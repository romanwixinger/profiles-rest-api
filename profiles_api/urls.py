from django.urls import path, include

from rest_framework.routers import DefaultRouter

from profiles_api import views

from profiles_api.topic import topic_api_view
from profiles_api.subtopic import subtopic_api_view
from profiles_api.question import question_api_view
from profiles_api.answer import answer_api_view
from profiles_api.test import test_api_view
from profiles_api.completed_test import completed_test_api_view
from profiles_api.theory_page import theory_page_api_view


router = DefaultRouter(trailing_slash=False)
router.register('profile', views.UserProfileViewSet)
# router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
# router.register('feed', views.UserProfileFeedViewSet)
# router.register('question', question_api_view.QuestionViewSet)
# router.register('subtopic', subtopic_api_view.SubtopicViewSet)
# router.register('topic', topic_api_view.TopicViewSet)
# router.register('answer', answer_api_view.AnswerViewSet)
# router.register('test', test_api_view.TestViewSet)
# router.register('completed-test', completed_test_api_view.CompletedTestViewSet)
# router.register('theory-page',  theory_page_api_view.TheoryPageViewSet)


urlpatterns = [
    # path('hello-view', views.HelloApiView.as_view()),
    path('login', views.UserLoginApiView.as_view()),
    path('custom-subtopic', subtopic_api_view.CustomSubtopicView.as_view()),
    path('recommended-subtopic', subtopic_api_view.RecommendedSubtopicView.as_view()),
    path('custom-question', question_api_view.QuestionView.as_view()),
    path('custom-topic', topic_api_view.TopicView.as_view()),
    path('custom-answer', answer_api_view.AnswerView.as_view()),
    path('custom-answer/<int:pk>', answer_api_view.AnswerView.as_view()),
    path('custom-test', test_api_view.TestView.as_view()),
    path('recommended-test', test_api_view.RecommendedTestView.as_view()),
    path('custom-completed-test', completed_test_api_view.CompletedTestView.as_view()),
    path('custom-completed-test/<int:pk>', completed_test_api_view.CompletedTestView.as_view()),
    path('custom-theory-page', theory_page_api_view.TheoryPageView.as_view()),
    path('recommended-theory-page', theory_page_api_view.RecommendedTheoryPageView.as_view()),
    path('', include(router.urls))
]
