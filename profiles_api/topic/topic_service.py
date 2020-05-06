from profiles_api.topic.topic_model import Topic

import random


class TopicService:

    @classmethod
    def search_topics(cls, query_params_dict: dict) -> [Topic]:
        """Get topics according to query parameters stored in a dict"""

        start = query_params_dict['start'] if 'start' in query_params_dict else None
        number = query_params_dict['number'] if 'number' in query_params_dict else None
        mode = query_params_dict['mode'] if 'mode' in query_params_dict else None

        topics = list(Topic.objects.all())

        if start is not None:
            topics = topics[min(abs(int(start)), len(topics)):]

        if number is not None:
            topics = topics[:max(0, min(int(number), len(topics)))]

        if mode is not None and mode == 'random':
            topics = list(topics)
            random.shuffle(topics)

        return topics
