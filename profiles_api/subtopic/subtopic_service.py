import random

from profiles_api.models import UserProfile
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.completed_test.completed_test_model import CompletedTest

from profiles_api.answer.answer_service import AnswerService
from profiles_api.knowledge_level.knowledge_level_service import KnowledgeLevelService


class SubtopicService:

    @classmethod
    def recommended_subtopics(cls, user: UserProfile, number: int = 100) -> [int]:
        """Evaluates all answers of the user and recommends subtopics accordingly. The subtopics are sorted according
        to the strongness of the recommendation."""

        subtopic_id_list = cls.subtopic_id_list()

        level_dict = KnowledgeLevelService.knowledge_level_list(user_id=user.id, subtopic_id_list=subtopic_id_list)
        number_dict = AnswerService.number_of_answers_list(user_id=user.id, subtopic_id_list=subtopic_id_list)

        sorted_subtopics = cls.sorted_subtopics(level_dict=level_dict, number_dict=number_dict)
        return sorted_subtopics[:number]

    @classmethod
    def search_subtopics(cls, query_params_dict: dict) -> [Subtopic]:
        """Get subtopics according to query parameters stored in a dict"""

        topic = query_params_dict['topic'] if 'topic' in query_params_dict else None
        topic_id = query_params_dict['topic_id'] if 'topic_id' in query_params_dict else None
        start = query_params_dict['start'] if 'start' in query_params_dict else None
        number = query_params_dict['number'] if 'number' in query_params_dict else None
        mode = query_params_dict['mode'] if 'mode' in query_params_dict else None

        if topic is not None:
            filter_dict = {'topic__name': topic}
            subtopics = Subtopic.objects.filter(**filter_dict)
        elif topic_id is not None:
            filter_dict = {'topic__id': topic_id}
            subtopics = Subtopic.objects.filter(**filter_dict)
        else:
            subtopics = Subtopic.objects.all()

        subtopics = list(subtopics)

        if mode == 'random':
            random.shuffle(subtopics)
        if start is not None:
            subtopics = subtopics[min(abs(int(start)), len(subtopics)):]
        if number is not None:
            subtopics = subtopics[:max(0, min(int(number), len(subtopics)))]

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
    def sorted_subtopics(cls, level_dict: dict, number_dict: dict):
        """Get a sorted list of subtopic ids: The earlier a subtopic appears, the more necessary it is to practice."""

        if set(level_dict.keys()) != set(number_dict.keys()):
            raise KeyError("The level_dict and the number_dict must have the same subtopics as keys.")

        weighted_level_list = []
        for subtopic_id in level_dict.keys():
            weighted_level_list.append(level_dict[subtopic_id] * number_dict[subtopic_id])

        sorted_subtopics = [subtopic for _, subtopic in sorted(zip(weighted_level_list, level_dict.keys()))]

        return sorted_subtopics

    @classmethod
    def get_subtopics(cls, subtopic_id_list: [int]) -> [Subtopic]:
        """Returns a list with the requested subtopics"""

        subtopic_list = []

        for subtopic_id in subtopic_id_list:
            filter_dict = {'id': subtopic_id}
            subtopic = Subtopic.objects.filter(**filter_dict)[0] \
                if Subtopic.objects.filter(**filter_dict).count() > 0 else None
            if subtopic is not None:
                subtopic_list.append(subtopic)
            else:
                raise LookupError("The subtopic with id " + str(subtopic_id) + " does not exist.")

        return list(subtopic_list)
