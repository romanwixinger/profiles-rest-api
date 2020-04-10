from profiles_api.models import UserProfile
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.test.test_model import Test
from profiles_api.completed_test.completed_test_model import CompletedTest
from profiles_api.theory_page.theory_page_model import TheoryPage


def get_recommended_subtopics(user: UserProfile, number: int = 2):
    """Evaluates all completed tests of the user and recommends subtopics accordingly"""

    subtopic_weight = 2
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

    subtopic_list = subtopic_dict.keys()
    ratio_list = [subtopic_dict[x]["ratio"] for x in subtopic_list]
    sorted_subtopics = [subtopic for _, subtopic in sorted(zip(ratio_list, subtopic_list))]

    print(subtopic_dict)
    print(sorted_subtopics)

    return sorted_subtopics[:number]


def get_recommended_theory_pages(user: UserProfile, number: int = 2):
    """"Evaluates all completed tests of the user and recommends theory pages accordingly"""

    recommended_subtopics = get_recommended_subtopics(user, number)
    if recommended_subtopics is None:
        return None

    recommended_theory_pages = []
    for recommended_subtopic in recommended_subtopics:
        filter_dict = {'subtopic': recommended_subtopic}
        theory_pages = TheoryPage.objects.filter(**filter_dict)
        if theory_pages is None:
            continue
        for theory_page in theory_pages:
            recommended_theory_pages.append(theory_page.id)

    print(recommended_theory_pages[:number])
    return recommended_theory_pages[:number]




