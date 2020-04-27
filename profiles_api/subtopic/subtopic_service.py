from profiles_api.models import UserProfile
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.completed_test.completed_test_model import CompletedTest
from profiles_api.answer.answer_service import AnswerService


class SubtopicService:

    @classmethod
    def get_recommended_subtopics(cls, user: UserProfile, number: int = 2) -> list:
        """Evaluates all completed tests of the user and recommends subtopics accordingly"""

        subtopic_dict = cls.subtopic_statistics(user)

        subtopic_list = subtopic_dict.keys()
        ratio_list = [subtopic_dict[x]["ratio"] for x in subtopic_list]
        sorted_subtopics = [subtopic for _, subtopic in sorted(zip(ratio_list, subtopic_list))]

        return sorted_subtopics[:number]

    @classmethod
    def get_subtopics(cls, query_params_dict: dict) -> list:
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
    def subtopic_statistics(cls, user: UserProfile):
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
            subtopic_dict[key]["total"] = subtopic_dict[key]["correct"] + subtopic_dict[key]["incorrect"]
            subtopic_dict[key]["ratio"] = subtopic_dict[key]["correct"] / (subtopic_dict[key]["correct"] + subtopic_dict[key]["incorrect"])

        return subtopic_dict

