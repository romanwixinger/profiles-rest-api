import random

from profiles_api.topic.topic_model import Topic


class TopicService:

    @classmethod
    def search_topics(cls, query_params_dict: dict) -> [Topic]:
        """Get topics according to query parameters stored in a dict"""

        start = query_params_dict['start'] if 'start' in query_params_dict else None
        number = query_params_dict['number'] if 'number' in query_params_dict else None
        mode = query_params_dict['mode'] if 'mode' in query_params_dict else None

        topics = list(Topic.objects.all())

        if mode == 'random':
            random.shuffle(topics)
        if start is not None:
            topics = topics[min(abs(int(start)), len(topics)):]
        if number is not None:
            topics = topics[:max(0, min(int(number), len(topics)))]

        return topics

    @classmethod
    def get_topics(cls, topic_id_list: [int]) -> [Topic]:
        """Returns a list with the requested topics"""

        topics = Topic.objects.filter(id__in=topic_id_list)
        topic_list = list(topics)

        return topic_list

