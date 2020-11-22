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
