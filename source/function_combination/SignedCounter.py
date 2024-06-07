from collections import defaultdict

class SignedCounter:
    """ counting elements while regarding their arithmetic sign """
    def __init__(self):
        self.counter = defaultdict(int)

    def update(self, iterable):
        """
        todo
        :param iterable:
        :return:
        """
        print("SignedCounter: update", iterable, type(iterable))
        for item in iterable:
            self.counter[item] += item.factor

    @property
    def items(self):
        """
        todo
        :return:
        """
        print("SignedCoutner: item", self.counter.items(), type(self.counter.items()))
        return self.counter.items()

