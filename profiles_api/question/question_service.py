from profiles_api.question.question_model import Question
from profiles_api.models import UserProfile
from profiles_api.subtopic.subtopic_model import Subtopic
from profiles_api.answer.answer_model import Answer

from profiles_api.proficiency.proficiency_service import ProficiencyService
from profiles_api.subtopic.subtopic_service import SubtopicService


class QuestionService:

    @classmethod
    def recommended_questions(cls, user: UserProfile, number: int = 2, length: int = 10) -> [int]:
        """Get a list of recommended question ids"""

        subtopic_id_list = Subtopic.subtopic_id_list()
        level_dict = ProficiencyService.proficiency_list(user_id=user.id, subtopic_id_list=subtopic_id_list)
        number_dict = Answer.number_of_answers_list(user_id=user.id, subtopic_id_list=subtopic_id_list)
        sorted_subtopics = SubtopicService.sorted_subtopics(level_dict=level_dict, number_dict=number_dict)

        subtopics = sorted_subtopics[:number]
        recommended_questions = []

        for subtopic_id in subtopics:

            difficulty = level_dict[subtopic_id]

            considered_questions = Question.questions_of_level(subtopic_id=subtopic_id, difficulty=difficulty,
                                                          number=2*length)
            answered_questions = Answer.search_answers_id(query_params_dict={
                'subtopic_id': subtopic_id,
                'difficulty': difficulty,
                'user_id': user.id
            })

            considered_questions = [question for question in considered_questions if question not in answered_questions]

            if len(considered_questions) < length:
                for level in [level for level in [1, 2, 3, 4, 5] if level != difficulty]:
                    considered_questions += Question.questions_of_level(subtopic_id=subtopic_id, difficulty=level, number=length)

            recommended_questions += considered_questions[:min(number, len(considered_questions))]

        return recommended_questions

    @classmethod
    def update_facilities(cls, question_id_list: [int]):
        """Update the facility of certain questions"""

        for question_id in question_id_list:
            question = Question.objects.get(pk=question_id)
            if question.time_diff_facility() > 10*60:
                cls.update_facility(question)

    @classmethod
    def update_facility(cls, question: Question):
        """Update the facility of a certain question"""

        correct = Answer.objects.filter(correct=True, question=question.id).count()
        false = Answer.objects.filter(correct=False, question=question.id).count()

        question.facility = correct/(correct + false) if correct + false > 0 else 0.5
        question.difficulty_updated_on.now()

        question.save()

        return












