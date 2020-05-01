from profiles_api.models import UserProfile
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.completed_test.completed_test_model import CompletedTest

from profiles_api.answer.answer_service import AnswerService
from profiles_api.knowledge_level.knowledge_level_service import KnowledgeLevelService
from profiles_api.question.question_service import QuestionService


class SubtopicService:

    @classmethod
    def recommended_subtopics(cls, user: UserProfile, number: int = 2) -> [int]:
        """Evaluates all answers of the user and recommends subtopics accordingly"""

        subtopic_id_list = cls.subtopic_id_list()

        level_dict = KnowledgeLevelService.knowledge_level_list(user_id=user.id, subtopic_id_list=subtopic_id_list)
        number_dict = AnswerService.number_of_answers_list(user_id=user.id, subtopic_id_list=subtopic_id_list)

        sorted_subtopics = cls.sorted_subtopics(level_dict=level_dict, number_dict=number_dict)
        return sorted_subtopics[:number]

    @classmethod
    def get_subtopics(cls, query_params_dict: dict) -> [Subtopic]:
        """Get subtopics according to query parameters stored in a dict"""

        topic = query_params_dict['topic'] if 'topic' in query_params_dict else None
        topic_id = query_params_dict['topic_id'] if 'topic_id' in query_params_dict else None
        start = query_params_dict['start'] if 'start' in query_params_dict else None
        number = query_params_dict['number'] if 'number' in query_params_dict else None

        if topic is not None:
            filter_dict = {'topic__name': topic}
            subtopics = Subtopic.objects.filter(**filter_dict)
        elif topic_id is not None:
            filter_dict = {'topic__id': topic_id}
            subtopics = Subtopic.objects.filter(**filter_dict)
        else:
            subtopics = Subtopic.objects.all()

        if start is not None:
            subtopics = subtopics[min(abs(int(start)), subtopics.count()):]

        if number is not None:
            subtopics = subtopics[:max(0, min(int(number), subtopics.count()))]

        return subtopics

    @classmethod
    def subtopic_statistics(cls, user: UserProfile) -> dict:
        """Return a dict with subtopics as key and dict with statistics as value."""

        subtopic_weight = 1
        dependency_weight = 1

        filter_dict = {'user_profile': user.id}
        completed_tests = CompletedTest.objects.filter(**filter_dict)
        if completed_tests is None:
            return None

        # Create a dict with subtopics as key and dict with relevant information as value.
        subtopic_dict = {}

        answers = AnswerService.search_answers(query_params_dict={'user_id': user.id})

        for answer in answers:
            if answer.question.subtopic_id not in subtopic_dict:
                subtopic_dict[answer.question.subtopic_id] = {"correct": 0, "incorrect": 0}

            if answer.correct:
                subtopic_dict[answer.question.subtopic_id]["correct"] += subtopic_weight
            else:
                subtopic_dict[answer.question.subtopic_id]["incorrect"] += subtopic_weight

            if answer.question.dependencies is None or answer.question.dependencies == []:
                continue
            for dependency in answer.question.dependencies.all():
                if dependency.id not in subtopic_dict:
                    subtopic_dict[dependency.id] = {"correct": 0, "incorrect": 0}

                if answer.correct:
                    subtopic_dict[dependency.id]["correct"] += dependency_weight
                else:
                    subtopic_dict[dependency.id]["incorrect"] += dependency_weight

        for key in subtopic_dict.keys():
            subtopic_dict[key]["total"] = subtopic_dict[key]["correct"] + subtopic_dict[key]["incorrect"]
            subtopic_dict[key]["ratio"] = subtopic_dict[key]["correct"] / (subtopic_dict[key]["correct"] + subtopic_dict[key]["incorrect"])

        return subtopic_dict

    @classmethod
    def subtopic_id_list(cls) -> [int]:
        """Get a list with all subtopic ids"""

        subtopic_id_list = [subtopic.id for subtopic in Subtopic.objects.all()]
        return subtopic_id_list

    @classmethod
    def subtopic_frequency_dict(cls,  question_id_list: [int]) -> dict:
        """Creates a dict with the occurring subtopics as keys and the number of occurrences as value"""

        subtopic_frequency_dict = {}

        question_list = QuestionService.get_questions(question_id_list)
        for question in question_list:
            if question.subtopic.id in subtopic_frequency_dict:
                subtopic_frequency_dict[question.subtopic.id] += 1
            else:
                subtopic_frequency_dict[question.subtopic.id] = 1

            dependencies = question.dependencies.all() if question.dependencies is not None else []
            for dependency in dependencies:
                if dependency.id in subtopic_frequency_dict:
                    subtopic_frequency_dict[dependency.id] += 1
                else:
                    subtopic_frequency_dict[dependency.id] = 1

        return subtopic_frequency_dict

    @classmethod
    def accordance(cls, recommended_subtopics: [int], subtopic_frequency_dict: dict) -> float:
        """Quantifies the accordance between a list of recommended subtopics and test"""

        if len(recommended_subtopics) == 0 or subtopic_frequency_dict == {}:
            return 0

        accordance = 0
        for subtopic_id in recommended_subtopics:
            accordance += subtopic_frequency_dict[subtopic_id] if subtopic_id in subtopic_frequency_dict else 0

        accordance /= len(subtopic_frequency_dict.keys())
        return accordance

    @classmethod
    def sorted_subtopics(cls, level_dict: dict, number_dict: dict):
        """Get a sorted list of subtopic ids: The earlier a subtopic appears, the more necessary it is to practice."""

        if set(level_dict.keys()) != set(number_dict.keys()):
            raise KeyError("The level_dict and the number_dict must have the same subtopics as keys.")

        weighted_level_list = []
        for subtopic_id in level_dict.keys():
            weighted_level_list.append(level_dict[subtopic_id] * number_dict[subtopic_id])

        sorted_subtopics = [subtopic for _, subtopic in sorted(zip(weighted_level_list, level_dict.keys()))]

        return sorted_subtopics

