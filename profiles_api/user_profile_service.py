import numpy as np

from profiles_api.models import UserProfile
from profiles_api.answer.answer_service import AnswerService
from profiles_api.knowledge_level.knowledge_level_service import KnowledgeLevelService


class UserProfileService:
    """Services that are related to the user"""

    @classmethod
    def get_user(cls, user_id: int):
        """Gets the user object by its id"""

        filter_dict = {'id': user_id}
        user = UserProfile.objects.filter(**filter_dict)[0]

        return user







