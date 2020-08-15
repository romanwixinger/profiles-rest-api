from profiles_api.models import UserProfile
from profiles_api.subtopic.subtopic_model import Subtopic

from profiles_api.answer.answer_service import AnswerService
from profiles_api.proficiency.proficiency_service import ProficiencyService


class SubtopicService:

    @classmethod
    def recommended_subtopics(cls, user: UserProfile, number: int = 100) -> [int]:
        """Evaluates all answers of the user and recommends subtopics accordingly. The subtopics are sorted according
        to the strongness of the recommendation."""

        subtopic_id_list = Subtopic.subtopic_id_list()

        level_dict = ProficiencyService.proficiency_list(user_id=user.id, subtopic_id_list=subtopic_id_list)
        number_dict = AnswerService.number_of_answers_list(user_id=user.id, subtopic_id_list=subtopic_id_list)

        sorted_subtopics = cls.sorted_subtopics(level_dict=level_dict, number_dict=number_dict)
        return sorted_subtopics[:number]

    @classmethod
    def sorted_subtopics(cls, level_dict: dict, number_dict: dict):
        """Get a sorted list of subtopic ids: The earlier a subtopic appears, the more necessary it is to practice."""

        if set(level_dict.keys()) != set(number_dict.keys()):
            raise KeyError("The level_dict and the number_dict must have the same subtopics as keys.")

        weighted_level_list = [level_dict[subtopic_id] * number_dict[subtopic_id] for subtopic_id in level_dict.keys()]
        sorted_subtopics = [subtopic for _, subtopic in sorted(zip(weighted_level_list, level_dict.keys()))]

        return sorted_subtopics


