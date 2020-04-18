from profiles_api.models import UserProfile
from profiles_api.user_profile_service import get_subtopic_statistics


def get_recommended_subtopics(user: UserProfile, number: int = 2):
    """Evaluates all completed tests of the user and recommends subtopics accordingly"""

    subtopic_dict = get_subtopic_statistics(user)

    subtopic_list = subtopic_dict.keys()
    ratio_list = [subtopic_dict[x]["ratio"] for x in subtopic_list]
    sorted_subtopics = [subtopic for _, subtopic in sorted(zip(ratio_list, subtopic_list))]

    return sorted_subtopics[:number]

