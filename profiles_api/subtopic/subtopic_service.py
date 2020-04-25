from profiles_api.models import UserProfile
from profiles_api.user_profile_service import get_subtopic_statistics
from profiles_api.subtopic.subtopic_model import Subtopic


class SubtopicService:

    @classmethod
    def get_recommended_subtopics(cls, user: UserProfile, number: int = 2) -> list:
        """Evaluates all completed tests of the user and recommends subtopics accordingly"""

        subtopic_dict = get_subtopic_statistics(user)

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


