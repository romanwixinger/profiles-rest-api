from profiles_api.completed_test.completed_test_model import CompletedTest
from profiles_api.answer.answer_model import Answer


def get_recommendations(completed_test: CompletedTest):
    """Evaluates answers and recommends subtopics accordingly"""


    answers = completed_test.answers.all()

    subtopic_dict = {}
    for answer in answers:
        if str(answer.question.subtopic_id) not in subtopic_dict:
            print(answer.question.subtopic_id)
            subtopic_dict[str(answer.question.subtopic_id)] = {"correct": 0, "incorrect": 0}

        if answer.correct:
            subtopic_dict[str(answer.question.subtopic_id)]["correct"] += 1
        else:
            subtopic_dict[str(answer.question.subtopic_id)]["incorrect"] += 1

    for key in subtopic_dict.keys():
        subtopic_dict[key]["ratio"] = subtopic_dict[key]["correct"] / (subtopic_dict[key]["correct"] + subtopic_dict[key]["incorrect"])

    print(subtopic_dict)

    return
