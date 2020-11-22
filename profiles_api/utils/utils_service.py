import random


class UtilsService:
    """Class for shared service functions"""

    @classmethod
    def select_items(cls, items: list, query_params_dict: dict) -> list:
        """Slices and shuffles the list of items"""

        if 'mode' in query_params_dict and query_params_dict['mode'] == 'random':
            random.shuffle(items)

        start = int(query_params_dict['start']) if 'start' in query_params_dict else 0
        stop = start + int(query_params_dict['number']) if 'number' in query_params_dict else None

        return items[start:stop]

    @classmethod
    def get_items(cls, item_id_list: [int], itemClass):
        """Returns a list with the requested items"""

        chunk_size = 200
        item_list = []

        for i in range(0, len(item_id_list), chunk_size):
            item_id_chunk = item_id_list[i:i + chunk_size]
            item_chunk = itemClass.objects.filter(id__in=item_id_chunk)
            item_list = item_list + list(item_chunk)

        return item_list
