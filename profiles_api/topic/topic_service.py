from profiles_api.topic.topic_model import Topic
from profiles_api.utils.utils_service import UtilsService


class TopicService:

    @classmethod
    def search_topics(cls, query_params_dict: dict) -> [Topic]:
        """Get topics according to query parameters stored in a dict"""

        topics = list(Topic.objects.all())
        topics = UtilsService.select_items(items=topics, query_params_dict=query_params_dict)

        return topics

    @classmethod
    def get_topics(cls, topic_id_list: [int]) -> [Topic]:
        """Returns a list with the requested topics"""

        topics = Topic.objects.filter(id__in=topic_id_list)
        return list(topics)
