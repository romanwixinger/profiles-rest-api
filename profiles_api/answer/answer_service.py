import re
import random
from typing import List, Set

from profiles_api.answer.answer_model import Answer
from profiles_api.question.question_model import Question

from profiles_api.topic.topic_service import TopicService


class AnswerService:

    @classmethod
    def perform_correction(cls, answer: Answer) -> Answer:
        validation_type = answer.question.validation_type
        if not answer.answers:
            answer.correct = False
            return answer

        if not validation_type or validation_type == 'standardValidation':
            return cls.__standard_validation(answer)

        if validation_type == 'multipleStrings':
            answer = cls.__multiple_string_validation(answer)
            return answer

        if validation_type == 'singleFraction':
            answer = cls.__single_fraction_validation(answer)
            return answer

        raise ValueError("Validation type of question is not valid")

    @classmethod
    def __standard_validation(cls, answer: Answer) -> Answer:
        answer.correct = answer.answers == answer.question.correctAnswers
        return answer

    @classmethod
    def __multiple_string_validation(cls, answer: Answer) -> Answer:
        wrong_answers = cls.__compare_answers(answer.answers.split(';'), answer.question.correctAnswers.split(';'))
        if not wrong_answers:
            answer.correct = True
            return answer

        answer.correct = False
        answer.comment = "Die Antwortfelder {} sind nicht korrekt".format(wrong_answers)

        return answer

    @classmethod
    def __compare_answers(cls, user_answers: List[str], correct_answers: List[str]) -> Set[int]:
        wrong_answer_list: Set[int] = set()
        for i in range(len(user_answers)):
            if user_answers[i] != correct_answers[i]:
                wrong_answer_list.add(i + 1)
        return wrong_answer_list

    @classmethod
    def __single_fraction_validation(cls, answer: Answer) -> Answer:
        try:
            user_answer = cls.__parse_float(answer.answers, "[/:]")
            correct_answer = cls.__parse_float(answer.question.correctAnswers, "(frac|/)")
            answer.correct = abs(user_answer - correct_answer) <= 1e-3
        except Exception:
            answer.comment = "Diese Frage konnte nicht korrigiert werden."
            answer.correct = False
        finally:
            return answer

    @classmethod
    def __parse_float(cls, float_str: str, regex: str) -> float:
        if not bool(re.search(regex, float_str)):
            return float(float_str)
        p = re.compile(r'\d+').findall(float_str)
        return float(int(p[0]) / int(p[1]))

    @classmethod
    def search_answers(cls, query_params_dict: dict) -> [Answer]:
        """Get the answers of a user according to query parameters stored in a dict"""

        answer_id_list = cls.search_answers_id(query_params_dict)
        answers = cls.get_answers(answer_id_list)

        return answers

    @classmethod
    def search_answers_id(cls, query_params_dict: dict) -> [int]:
        """Get the answers of a user according to query parameters stored in a dict"""

        if 'user_id' not in query_params_dict or query_params_dict['user_id'] == '':
            raise Exception("The class method search_answers must only be used with a user_id.")

        filter_args = {'user_id': 'user_profile', 'question_id': 'question__id', 'topic_id': 'question__topic',
                       'subtopic_id': 'question__subtopic', 'difficulty': 'question__difficulty'}

        filter_dict = {filter_args[key]: query_params_dict[key] for key in filter_args.keys()
                       if key in query_params_dict}

        answer_id_list = list(Answer.objects.filter(**filter_dict).values_list('id', flat=True))
        answer_id_list = TopicService.select_items(items=answer_id_list, query_params_dict=query_params_dict)

        return answer_id_list

    @classmethod
    def get_answers(cls, answer_id_list: int):
        """Returns a list with the requested answers"""

        answers = Answer.objects.filter(id__in=answer_id_list)
        return list(answers)

    @classmethod
    def get_all_answers(cls, question_id: int, query_params_dict: dict) -> [Answer]:
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
            number_of_answers = AnswerService.number_of_answers(user_id=user_id, subtopic_id=subtopic_id)
            number_dict[subtopic_id] = number_of_answers

        return number_dict

    @classmethod
    def difficulty_list(cls, question_id_list: [int], update: bool = False) -> [int]:
        """Takes a list of question ids and return a list of their difficulties"""

        difficulty_list = []

        for question_id in question_id_list:
            question = Question.objects.get(pk=question_id)

            if update:
                question.difficulty = cls.difficulty(question_id)
            else:
                difficulty = question.difficulty
            difficulty_list.append(difficulty)

        return difficulty_list

    @classmethod
    def difficulty(cls, question_id: int) -> int:
        """Calculate the difficulty of a question. Possible values are in the set {1, 2, 3, 4, 5}."""

        facility = cls.facility(question_id=question_id)
        set_difficulty = cls.set_difficulty(question_id=question_id)

        fac_difficulty = int(6 - facility * 5)

        difficulty = int(0.5 * set_difficulty + 0.5 * fac_difficulty + 0.5)
        difficulty = max(1, min(5, difficulty))

        return difficulty

    @classmethod
    def facility(cls, question_id: int) -> float:
        """Get the facility of a question. Possible values are in the range [0,1]."""

        answers = cls.get_all_answers(question_id=question_id, query_params_dict={})

        correct = 0
        incorrect = 0

        for answer in answers:
            if answer.correct:
                correct += 1
            else:
                incorrect += 1

        facility = correct / (correct + incorrect)
        return facility

    @classmethod
    def set_difficulty(cls, question_id: int) -> int:
        """Retrieve the set difficulty of a question"""

        question = Question.objects.get(pk=question_id)
        set_difficulty = question.set_difficulty

        return set_difficulty

    @classmethod
    def update_difficulty(cls):
        """Update the difficulty estimate of all questions"""

        questions = Question.objects.all()

        for question in questions:
            question.difficulty = cls.difficulty(question_id=question.id)

        return

