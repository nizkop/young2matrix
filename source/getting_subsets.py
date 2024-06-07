from typing import List
from itertools import chain, combinations, permutations


def permutations_of_subsets(array: List[List[int]], group_number:int) -> List[tuple]:
    """ combinations of possible subsets;
    differentiate between different sorting in these combinations,
    and sort out combinations, if they obviously are not going to fit into young tableaus
    :param array: lists of subsets
    :param group_number: number of the choosen permutation group
    :return: list of fitting combinations
    """
    all_combinations = chain.from_iterable(combinations(array, r) for r in range(len(array) + 1))
    # remove dimensional-unfitting examples:
    unique_combinations = []
    for combo in all_combinations:
        all_numbers = [element for sublist in combo for element in sublist]
        if len(set(all_numbers)) == len(all_numbers) and len(all_numbers) == group_number:
            unique_combinations.append(combo)
    # differentiate between sorting:
    return [permutation for x in unique_combinations for permutation in permutations(x)]




def get_powerset(array: List) -> List:
    """ getting a list of all subsets of array
    :param array: (mathematical) set
    :return: list of all subsets 
    """
    subsets = []
    for r in range(len(array) + 1):
        subsets.extend(combinations(array, r))
    return list(subsets)