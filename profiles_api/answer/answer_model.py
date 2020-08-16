from django.db import models
from django.conf import settings

from profiles_api.question.question_model import Question

from profiles_api.utils.utils_service import UtilsService


class Answer(models.Model):
    """Answer"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    duration = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=0)  # in seconds
    answers = models.CharField(max_length=1024, blank=True)

    # Fields set after correction
    correct = models.BooleanField(blank=True, default=False)
    skipped = models.BooleanField(blank=True, default=False)
    comment = models.CharField(max_length=1024, blank=True, default="")

    def __str__(self):
        """Return the model as a string"""
        return self.answers

    @classmethod
    def search_answers(cls, query_params_dict: dict) -> []:
        """Get the answers of a user according to query parameters stored in a dict"""

        answer_id_list = cls.search_answers_id(query_params_dict)
        answers = cls.get_answers(answer_id_list)

        return answers

    @classmethod
    def search_answers_id(cls, query_params_dict: dict) -> [int]:
        """Get the answers of a user according to query parameters stored in a dict"""

        filter_args = {'user_id': 'user_profile', 'question_id': 'question__id', 'topic_id': 'question__topic',
                       'subtopic_id': 'question__subtopic', 'difficulty': 'question__difficulty', 'id': 'id'}

        filter_dict = {filter_args[key]: query_params_dict[key] for key in filter_args.keys()
                       if key in query_params_dict}

        answer_id_list = list(Answer.objects.filter(**filter_dict).values_list('id', flat=True))
        answer_id_list = UtilsService.select_items(items=answer_id_list, query_params_dict=query_params_dict)

        return answer_id_list

    @classmethod
    def get_answers(cls, answer_id_list: [int]):
        """Returns a list with the requested answers"""

        answers = Answer.objects.filter(id__in=answer_id_list)
        return list(answers)

    @classmethod
    def get_all_answers(cls, question_id: int, query_params_dict: dict) -> []:
        """Get the answers of all user to a specific question"""

        answers = Answer.objects.filter(**{'question__id': question_id})

        number = query_params_dict['number'] if 'number' in query_params_dict else None
        if number is not None:
            answers = answers[:number]

        return answers

    @classmethod
    def number_of_answers(cls, user_id: int, subtopic_id: int) -> int:
        """Get the number of answers of a user to questions of a certain subtopic"""

        filter_dict = {'user_profile': user_id, 'question__subtopic_id': subtopic_id}
        return Answer.objects.filter(**filter_dict).count()

    @classmethod
    def number_of_answers_list(cls, user_id: int, subtopic_id_list: [int]) -> dict:
        """Get the number of answers of a user to questions of a certain subtopic"""

        number_dict = {}

        for subtopic_id in subtopic_id_list:
            number_of_answers = Answer.number_of_answers(user_id=user_id, subtopic_id=subtopic_id)
            number_dict[subtopic_id] = number_of_answers

        return number_dict





