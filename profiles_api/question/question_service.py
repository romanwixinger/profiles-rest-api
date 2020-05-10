import random

from profiles_api.question.question_model import Question
from profiles_api.models import UserProfile
from profiles_api.answer.answer_service import AnswerService
from profiles_api.knowledge_level.knowledge_level_service import KnowledgeLevelService
from profiles_api.subtopic.subtopic_service import SubtopicService


class QuestionService:

    @classmethod
    def search_questions(cls, query_params_dict: dict) -> list:
        """Get questions according to query parameters stored in a dict"""

        topic = query_params_dict['topic'] if 'topic' in query_params_dict else None
        topic_id = query_params_dict['topic_id'] if 'topic_id' in query_params_dict else None
        subtopic = query_params_dict['subtopic'] if 'subtopic' in query_params_dict else None
        subtopic_id = query_params_dict['subtopic_id'] if 'subtopic_id' in query_params_dict else None
        start = query_params_dict['start'] if 'start' in query_params_dict else None
        number = query_params_dict['number'] if 'number' in query_params_dict else None
        mode = query_params_dict['mode'] if 'mode' in query_params_dict else None
        difficulty =  query_params_dict['difficulty'] if 'difficulty' in query_params_dict else None

        filter_dict = {}
        if topic is not None:
            filter_dict['topic__name'] = topic
        if topic_id is not None:
            filter_dict['topic__id'] = topic_id
        if subtopic is not None:
            filter_dict['subtopic__name'] = subtopic
        if subtopic_id is not None:
            filter_dict['subtopic__id'] = subtopic_id
        if difficulty is not None:
            filter_dict['difficulty'] = difficulty

        questions = list(Question.objects.filter(**filter_dict))

        if mode == 'random':
            random.shuffle(questions)
        if start is not None:
            questions = questions[min(abs(int(start)), len(questions)):]
        if number is not None:
            questions = questions[:max(0, min(int(number), len(questions)))]

        return questions

    @classmethod
    def get_questions(cls, question_id_list: [int]) -> [Question]:
        """Returns a list with the requested questions"""

        questions = Question.objects.filter(id__in=question_id_list)
        question_list = list(questions)

        return question_list

    @classmethod
    def recommended_questions(cls, user: UserProfile, number: int = 2, length: int = 10) -> [int]:
        """Get a list of recommended question ids"""

        subtopic_id_list = SubtopicService.subtopic_id_list()
        level_dict = KnowledgeLevelService.knowledge_level_list(user_id=user.id, subtopic_id_list=subtopic_id_list)
        number_dict = AnswerService.number_of_answers_list(user_id=user.id, subtopic_id_list=subtopic_id_list)
        sorted_subtopics = SubtopicService.sorted_subtopics(level_dict=level_dict, number_dict=number_dict)

        subtopics = sorted_subtopics[:min(number, len(sorted_subtopics))]
        recommended_questions = []

        for subtopic_id in subtopics:

            difficulty = level_dict[subtopic_id]

            considered_questions = cls.questions_of_level(subtopic_id=subtopic_id, difficulty=difficulty,
                                                   number=2*length)
            answered_questions = AnswerService.search_answers_id(query_params_dict={
                'subtopic_id': subtopic_id,
                'difficulty': difficulty,
                'user_id': user.id
            })

            considered_questions = [question for question in considered_questions if question not in answered_questions]

            if len(considered_questions) < length:
                for level in [level for level in [1, 2, 3, 4, 5] if level != difficulty]:
                    considered_questions += cls.questions_of_level(subtopic_id=subtopic_id, difficulty=level, number=length)

            recommended_questions += considered_questions[:min(number, len(considered_questions))]

        return recommended_questions

    @classmethod
    def questions_of_level(cls, subtopic_id: int, difficulty: int, number: int = -1) -> [int]:
        """Get a number of question ids of a subtopic of a certain level of difficulty"""

        filter_dict = {'subtopic__id': subtopic_id, 'difficulty': difficulty}
        questions = Question.objects.filter(**filter_dict).values_list('id', flat=True)

        question_list = list(questions)

        if number == -1:
            return question_list

        return question_list[:max(0, min(int(number), questions.count()))]










