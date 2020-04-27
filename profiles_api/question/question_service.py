from profiles_api.question.question_model import Question


class QuestionService:

    @classmethod
    def get_questions(cls, query_params_dict: dict) -> list:
        """Get questions according to query parameters stored in a dict"""

        topic = query_params_dict['topic'] if 'topic' in query_params_dict else None
        topic_id = query_params_dict['topic_id'] if 'topic_id' in query_params_dict else None
        subtopic = query_params_dict['subtopic'] if 'subtopic' in query_params_dict else None
        subtopic_id = query_params_dict['subtopic_id'] if 'subtopic_id' in query_params_dict else None
        start = query_params_dict['start'] if 'start' in query_params_dict else None
        number = query_params_dict['number'] if 'number' in query_params_dict else None

        filter_dict = {}
        if topic is not None:
            filter_dict['topic__name'] = topic
        if topic_id is not None:
            filter_dict['topic__id'] = topic_id
        if subtopic is not None:
            filter_dict['subtopic__name'] = subtopic
        if subtopic_id is not None:
            filter_dict['subtopic__id'] = subtopic_id
        questions = Question.objects.filter(**filter_dict)

        if start is not None:
            questions = questions[min(abs(int(start)), questions.count()):]
        if number is not None:
            questions = questions[:max(0, min(int(number), questions.count()))]

        return questions

    @classmethod
    def difficulty_list(cls, question_id_list: [int]) -> [int]:
        """Takes a list of question ids and return a list of their difficulties"""

        difficulty_list = []

        for question_id in question_id_list:
            difficulty = QuestionService.difficulty(question_id)
            difficulty_list.append(difficulty)

        return difficulty_list

    @classmethod
    def difficulty(cls, question_id: int) -> int:
        """Get the difficulty of a question."""

        return 3






