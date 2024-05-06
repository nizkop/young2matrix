from collections import defaultdict

class SignedCounter:
    """ counting elements while regarding their arithmetic sign """
    def __init__(self):
        self.counter = defaultdict(int)

    def update(self, iterable):
        for item in iterable:
            self.counter[item] += item.factor

    def items(self):
        return self.counter.items()

