
from itertools import chain, combinations, permutations


def powerset(iterable, group_number:int):
    s = list(iterable)
    all_combinations = chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))
    # remove dimensional-unfitting examples:
    unique_combinations = []
    for combo in all_combinations:
        all_numbers = [element for sublist in combo for element in sublist]
        if len(set(all_numbers)) == len(all_numbers) and len(all_numbers) == group_number:
            unique_combinations.append(combo)
    # differentiate between sorting:
    return [list(permutation) for x in unique_combinations for permutation in permutations(x)]




def find_subsets(array):
    subsets = []
    for r in range(len(array) + 1):
        subsets.extend(combinations(array, r))
    return subsets