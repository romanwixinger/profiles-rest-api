from profiles_api.completed_test.completed_test_model import CompletedTest
from profiles_api.subtopic.subtopic_model import Subtopic

from profiles_api.utils.utils_service import UtilsService


class CompletedTestService:
    """Service class for completed tests"""

    @classmethod
    def get_recommended_subtopics(cls, completed_test: CompletedTest, number: int = 2) -> [Subtopic]:
        """Evaluates answers and recommends subtopics accordingly"""

        subtopic_weight = 2
        dependency_weight = 1

        answers = completed_test.answers.all()

        # Create a dict with subtopics as key and dict with relevant information as value.
        subtopic_dict = {}
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

        subtopic_list = subtopic_dict.keys()
        ratio_list = [subtopic_dict[x]["ratio"] for x in subtopic_list]
        sorted_subtopics = [subtopic for _, subtopic in sorted(zip(ratio_list, subtopic_list))]

        for subtopic_id in sorted_subtopics[:number]:
            filter_dict = {'id': subtopic_id}
            subtopic = Subtopic.objects.filter(**filter_dict)[0]
            completed_test.recommendedSubtopics.add(subtopic)

        completed_test.save()

        return

    @classmethod
    def search_completed_tests(cls, query_params_dict: dict) -> [CompletedTest]:
        """Get the completed tests of a user according to query parameters stored in a dict"""

        filter_dict = {'user_profile': query_params_dict['user_id']} if 'user_id' in query_params_dict else {}

        if 'id' in query_params_dict:
            filter_dict['id'] = query_params_dict['id']
            if CompletedTest.objects.filter(**filter_dict).count() == 0:
                raise LookupError

        if 'state' in query_params_dict:
            filter_dict['state'] = query_params_dict['state']

        completed_tests_list = list(CompletedTest.objects.filter(**filter_dict))
        completed_tests_list = UtilsService.select_items(items=completed_tests_list, query_params_dict=query_params_dict)

        return completed_tests_list

    @classmethod
    def get_completed_tests(cls, completed_test_id_list: [int]) -> [CompletedTest]:
        """Returns a list with the requested completed tests"""

        completed_tests = CompletedTest.objects.filter(id__in=completed_test_id_list)
        return list(completed_tests)
