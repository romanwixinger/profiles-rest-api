from profiles_api.models import UserProfile
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.test.test_model import Test
from profiles_api.completed_test.completed_test_model import CompletedTest
from profiles_api.theory_page.theory_page_model import TheoryPage


def get_subtopic_statistics(user: UserProfile):
    """Return a  a dict with subtopics as key and dict with statistics as value."""

    subtopic_weight = 1
    dependency_weight = 1

    filter_dict = {'user_profile': user.id}
    completed_tests = CompletedTest.objects.filter(**filter_dict)
    if completed_tests is None:
        return None

    # Create a dict with subtopics as key and dict with relevant information as value.
    subtopic_dict = {}

    for completed_test in completed_tests:

        answers = completed_test.answers.all()

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

    return subtopic_dict


def get_user(user_id: int):
    """Gets the user object by its id"""

    filter_dict = {'id': user_id}
    user = UserProfile.objects.filter(**filter_dict)[0]

    return user



