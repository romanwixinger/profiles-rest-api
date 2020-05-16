import random

from profiles_api.topic.topic_model import Topic


class TopicService:

    @classmethod
    def search_topics(cls, query_params_dict: dict) -> [Topic]:
        """Get topics according to query parameters stored in a dict"""

        topics = list(Topic.objects.all())

        if 'mode' in query_params_dict and query_params_dict['mode'] == 'random':
            random.shuffle(topics)

        start = int(query_params_dict['start']) if 'start' in query_params_dict else 0
        stop = start + int(query_params_dict['number']) if 'number' in query_params_dict else None

        return topics[start:stop]

    @classmethod
    def get_topics(cls, topic_id_list: [int]) -> [Topic]:
        """Returns a list with the requested topics"""

        topics = Topic.objects.filter(id__in=topic_id_list)
        return list(topics)

