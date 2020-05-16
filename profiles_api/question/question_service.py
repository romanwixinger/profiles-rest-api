from profiles_api.question.question_model import Question
from profiles_api.models import UserProfile

from profiles_api.topic.topic_service import TopicService
from profiles_api.answer.answer_service import AnswerService
from profiles_api.knowledge_level.knowledge_level_service import KnowledgeLevelService
from profiles_api.subtopic.subtopic_service import SubtopicService


class QuestionService:

    @classmethod
    def search_questions(cls, query_params_dict: dict) -> list:
        """Get questions according to query parameters stored in a dict"""

        filter_args = {'question': 'question', 'topic': 'topic_name', 'topic_id': 'topic__id',
                       'difficulty': 'difficulty', 'subtopic': 'subtopic__name', 'subtopic_id': 'subtopic'}

        filter_dict = {filter_args[key]: query_params_dict[key] for key in filter_args.keys()
                       if key in query_params_dict}

        questions = list(Question.objects.filter(**filter_dict))
        questions = TopicService.select_items(questions, query_params_dict)

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










