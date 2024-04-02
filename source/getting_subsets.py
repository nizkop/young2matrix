

from itertools import chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def find_subsets(array):
    subsets = []
    for r in range(len(array) + 1):
        subsets.extend(combinations(array, r))
    return subsets