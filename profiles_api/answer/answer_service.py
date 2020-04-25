import re
from typing import List, Set

from profiles_api.answer.answer_model import Answer


class AnswerService:

    @classmethod
    def perform_correction(cls, answer: Answer) -> Answer:
        validation_type = answer.question.validation_type
        if not answer.answers:
            answer.correct = False
            return answer

        if not validation_type or validation_type == 'standardValidation':
            return cls.__standard_validation(answer)

        if validation_type == 'multipleString':
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
        wrong_answer_list = Set[int]
        for i in range(len(user_answers)):
            if user_answers[i] != correct_answers[i]:
                wrong_answer_list.append(i + 1)
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
    def get_answers(cls, query_params_dict: dict) -> list:
        """Get answers according to query parameters stored in a dict"""

        user_id = query_params_dict['user_id'] if 'user_id' in query_params_dict else None
        if user_id is None or user_id == '':
            raise Exception("The class method get_answers must only be used with a user_id.")

        start = query_params_dict['start'] if 'start' in query_params_dict else None
        number = query_params_dict['number'] if 'number' in query_params_dict else None
        question_id = query_params_dict['question_id'] if 'question_id' in query_params_dict else None
        topic_id = query_params_dict['topic_id'] if 'topic_id' in query_params_dict else None
        subtopic_id = query_params_dict['subtopic_id'] if 'subtopic_id' in query_params_dict else None

        filter_dict = dict()
        if question_id is not None and question_id != '':
            filter_dict['question__id'] = question_id
        if topic_id is not None and question_id != '':
            filter_dict['question__topic'] = topic_id
        if subtopic_id is not None and question_id != '':
            filter_dict['question__subtopic'] = subtopic_id
        answers = Answer.objects.filter(**filter_dict)

        if start is not None:
            answers = answers[min(abs(int(start)), answers.count()):]
        if number is not None:
            answers = answers[:max(0, min(int(number), answers.count()))]

        return answers

