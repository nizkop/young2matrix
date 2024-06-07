from collections import defaultdict
from collections.abc import dict_items
from typing import List


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

    @property
    def items(self) -> dict_items:
        """
        :return: collected (= identical) items/functions/...
        """
        return self.counter.items()

