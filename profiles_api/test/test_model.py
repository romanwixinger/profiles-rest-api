from django.db import models
from django.conf import settings

import random

from profiles_api.models import UserProfile
from profiles_api.question.question_model import Question

from profiles_api.utils.utils_service import UtilsService

class Test(models.Model):
    """Generic test"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    questions = models.ManyToManyField(Question)
    title = models.CharField(max_length=255)
    html = models.CharField(max_length=8191, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    creation_type = models.CharField(max_length=255, default='standard')

    def __str__(self):
        """Return the model as a string"""
        return self.title

    @classmethod
    def get_tests(cls, test_id_list: [int]) -> []:
        """Gets specific tests"""

        test_list = UtilsService.get_items(test_id_list, Test)

        return test_list

    @classmethod
    def search_tests(cls, query_params_dict: dict) -> list:
        """Get tests according to query parameters stored in a dict"""

        test_id = query_params_dict['id'] if 'id' in query_params_dict else None
        title = query_params_dict['title'] if 'title' in query_params_dict else None
        start = query_params_dict['start'] if 'start' in query_params_dict else None
        number = query_params_dict['number'] if 'number' in query_params_dict else None
        mode = query_params_dict['mode'] if 'mode' in query_params_dict else None
        creation_type = query_params_dict['creation_type'] if 'creation_type' in query_params_dict else None

        filter_dict = {'creation_type': creation_type} if creation_type is not None else {}

        if test_id is not None and ((isinstance(test_id, str) and test_id.isdigit())
                                    or isinstance(test_id, int)
                                    or isinstance(test_id, float)):
            filter_dict['id'] = int(test_id)
        if title is not None:
            filter_dict['title'] = title

        tests = list(Test.objects.filter(**filter_dict))

        if mode == 'random':
            random.shuffle(tests)
        if start is not None:
            tests = tests[min(abs(int(start)), len(tests)):]
        if number is not None:
            tests = tests[:max(0, min(int(number), len(tests)))]

        return tests

    @classmethod
    def solved_tests(cls, user_id) -> [int]:
        """Get a list with the ids of all the tests that have been solved"""

        filter_dict = {'user_profile': user_id}
        completed_tests = cls.objects.filter(**filter_dict)
        solved_tests = [completed_test.id for completed_test in completed_tests]

        unique_solved_tests = {}
        for solved_test in solved_tests:
            unique_solved_tests[solved_test] = 1

        return list(unique_solved_tests.keys())

    @classmethod
    def create_test(cls, user_id: int, question_id_list: [int], title: str, html: str = "", creation_type: str="standard"):
        """Create a test"""

        filter_dict = {'id': user_id}
        user = UserProfile.objects.filter(**filter_dict)[0]

        test = Test.objects.create(
            user_profile=user,
            title=title,
            html=html,
            creation_type=creation_type,
        )

        test.save()

        for question_id in question_id_list:
            filter_dict = {'id': question_id}
            question = Question.objects.filter(**filter_dict)[0] \
                if Question.objects.filter(**filter_dict).count() > 0 else None
            if question is None:
                raise LookupError
            else:
                test.questions.add(question)

        test.save()

        return test
