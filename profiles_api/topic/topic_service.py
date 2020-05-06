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

    @classmethod
    def get_topics(cls, topic_id_list: [int]) -> [Topic]:
        """Returns a list with the requested topics"""

        topic_list = []

        for topic_id in topic_id_list:
            filter_dict = {'id': topic_id}
            topic = Topic.objects.filter(**filter_dict)[0] \
                if Topic.objects.filter(**filter_dict).count() > 0 else None
            if topic is not None:
                topic_list.append(topic)
            else:
                raise LookupError("The topic with id " + str(topic_id) + " does not exist.")

        return topic_list
