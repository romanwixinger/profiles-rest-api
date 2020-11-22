from django.db import models
from django.conf import settings

from profiles_api.answer.answer_model import Answer
from profiles_api.test.test_model import Test

from profiles_api.utils.utils_service import UtilsService


class CompletedTest(models.Model):
    """Completed test"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    answers = models.ManyToManyField(Answer, blank=True)
    state = models.CharField(max_length=255, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    duration = models.DecimalField(max_digits=8, decimal_places=2, blank=True)  # in seconds
    comment = models.CharField(max_length=1024, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        """Return the model as a string"""
        return "Test started on " + self.created_on.__str__() + "."

    @classmethod
    def search_completed_tests(cls, query_params_dict: dict) -> []:
        """Get the completed tests of a user according to query parameters stored in a dict"""

        filter_dict = {'user_profile': query_params_dict['user_id']} if 'user_id' in query_params_dict else {}

        if 'id' in query_params_dict:
            filter_dict['id'] = query_params_dict['id']
            if cls.objects.filter(**filter_dict).count() == 0:
                raise LookupError

        if 'state' in query_params_dict:
            filter_dict['state'] = query_params_dict['state']

        completed_tests_list = list(cls.objects.filter(**filter_dict))
        completed_tests_list = UtilsService.select_items(items=completed_tests_list, query_params_dict=query_params_dict)

        return completed_tests_list

    @classmethod
    def get_completed_tests(cls, completed_test_id_list: [int]) -> []:
        """Returns a list with the requested completed tests"""

        completed_tests = cls.objects.filter(id__in=completed_test_id_list)
        return list(completed_tests)
