import random

from profiles_api.topic.topic_model import Topic


class TopicService:

    @classmethod
    def search_topics(cls, query_params_dict: dict) -> [Topic]:
        """Get topics according to query parameters stored in a dict"""

        topics = list(Topic.objects.all())
        topics = cls.select_items(items=topics, query_params_dict=query_params_dict)

        return topics

    @classmethod
    def get_topics(cls, topic_id_list: [int]) -> [Topic]:
        """Returns a list with the requested topics"""

        topics = Topic.objects.filter(id__in=topic_id_list)
        return list(topics)

    @classmethod
    def select_items(cls, items: list, query_params_dict: dict) -> list:
        """Slices and shuffles the list of items"""

        if 'mode' in query_params_dict and query_params_dict['mode'] == 'random':
            random.shuffle(items)

        start = int(query_params_dict['start']) if 'start' in query_params_dict else 0
        stop = start + int(query_params_dict['number']) if 'number' in query_params_dict else None

        return items[start:stop]
