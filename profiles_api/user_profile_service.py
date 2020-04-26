import numpy as np

from profiles_api.models import UserProfile
from profiles_api.completed_test.completed_test_model import CompletedTest
from profiles_api.answer.answer_service import AnswerService
from profiles_api.knowledge_level.knowledge_level_service import KnowledgeLevelService


class UserProfileService:
    """Services that are related to the user"""

    @classmethod
    def get_subtopic_statistics(cls, user: UserProfile):
        """Return a dict with subtopics as key and dict with statistics as value."""

        subtopic_weight = 1
        dependency_weight = 1

        filter_dict = {'user_profile': user.id}
        completed_tests = CompletedTest.objects.filter(**filter_dict)
        if completed_tests is None:
            return None

        # Create a dict with subtopics as key and dict with relevant information as value.
        subtopic_dict = {}

        answers = AnswerService.get_answers(query_params_dict={'user_id': user.id})

        for answer in answers:
            if str(answer.question.subtopic_id) not in subtopic_dict:
                subtopic_dict[str(answer.question.subtopic_id)] = {"correct": 0, "incorrect": 0}

            if answer.correct:
                subtopic_dict[str(answer.question.subtopic_id)]["correct"] += subtopic_weight
            else:
                subtopic_dict[str(answer.question.subtopic_id)]["incorrect"] += subtopic_weight

            if answer.question.dependencies is None or answer.question.dependencies == []:
                continue
            for dependency in answer.question.dependencies.all():
                if str(dependency.id) not in subtopic_dict:
                    subtopic_dict[str(dependency.id)] = {"correct": 0, "incorrect": 0}

                if answer.correct:
                    subtopic_dict[str(dependency.id)]["correct"] += dependency_weight
                else:
                    subtopic_dict[str(dependency.id)]["incorrect"] += dependency_weight

        for key in subtopic_dict.keys():
            subtopic_dict[key]["ratio"] = subtopic_dict[key]["correct"] / (subtopic_dict[key]["correct"] + subtopic_dict[key]["incorrect"])
            # print("Subtopic_id: " + key + ", level: ", UserProfileService.get_knowledge_level(user_id=user.id, subtopic_id=int(key)))

        return subtopic_dict

    @classmethod
    def get_user(cls, user_id: int):
        """Gets the user object by its id"""

        filter_dict = {'id': user_id}
        user = UserProfile.objects.filter(**filter_dict)[0]

        return user

    @classmethod
    def get_knowledge_level(cls, user_id: int, subtopic_id: int):
        """Get the knowledge level of a user in a specific subtopic"""

        query_params_dict = {'user_id': user_id,
                             'subtopic_id': subtopic_id}
        answers = AnswerService.get_answers(query_params_dict)

        correct = 0
        incorrect = 0
        for answer in answers:
            if answer.correct:
                correct += 1
            else:
                incorrect += 1

        data = np.array([[3], [correct], [incorrect]])
        level = KnowledgeLevelService.knowledge_level(data)

        return level







