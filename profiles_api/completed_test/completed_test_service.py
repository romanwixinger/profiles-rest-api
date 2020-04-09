from profiles_api.completed_test.completed_test_model import CompletedTest
from profiles_api.answer.answer_model import Answer
from profiles_api.subtopic.subtopic_model import Subtopic


def get_recommendations(completed_test: CompletedTest, number: int = 2):
    """Evaluates answers and recommends subtopics accordingly"""

    suptopic_weight = 2
    dependency_weight = 1

    answers = completed_test.answers.all()

    # Create a dict with subtopics as key and dict with relevant information as value.
    subtopic_dict = {}
    for answer in answers:
        if str(answer.question.subtopic_id) not in subtopic_dict:
            subtopic_dict[str(answer.question.subtopic_id)] = {"correct": 0, "incorrect": 0}

        if answer.correct:
            subtopic_dict[str(answer.question.subtopic_id)]["correct"] += suptopic_weight
        else:
            subtopic_dict[str(answer.question.subtopic_id)]["incorrect"] += suptopic_weight

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

    for subtopic_id in sorted_subtopics[:number]:
        filter_dict = {'id': subtopic_id}
        subtopic = Subtopic.objects.filter(**filter_dict)[0]
        completed_test.recommendedSubtopics.add(subtopic)

    completed_test.save()

    return
