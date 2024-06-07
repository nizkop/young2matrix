from collections import defaultdict
from typing import List, Any


class SignedCounter:
    """ counting elements while regarding their arithmetic sign """
    def __init__(self):
        self.counter = defaultdict(int)

    def update(self, iterable: List) -> None:
        """
        counting a new term (with the same functionality), but considering its pre-factor
        :param iterable: list of integral objects (e.g. hamilton integrals)
        """
        for item in iterable:
            self.counter[item] += item.factor

    def items(self) -> Any:#dict_items
        """
        :return: collected (= identical) items/functions/... (dict_items)
        """
        return self.counter.items()

