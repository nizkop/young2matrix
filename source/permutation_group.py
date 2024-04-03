from typing import List
import itertools

from source.getting_subsets import find_subsets, powerset
from source.overview_pdf import overview_pdf
from source.chemical_standard_tableau import chemical_standard_tableau
from source.standard_tableau import standard_tableau
from source.young_tableau import young_tableau


class permutation_group(object):
    def __init__(self, permutation_group:int=0):
        self.permutation_group: int = permutation_group
        self.tableaus : List[young_tableau] = []
        self.standard_tableaus : List[chemical_standard_tableau] = []
        self.overview = overview_pdf()

    def print(self):
        pass

    def find_tableaus(self):
        pass

    def get_overview_pdf(self, title:str)->None:
        pass

    def get_all_standard_tableaus(self)->None:
        """
        :return: None, because result is written into self.standard_tableaus
        """
        # find subsets of all combinations:
        numbers = list(range(1, self.permutation_group + 1))
        subsets = [list(subset) for subset in find_subsets(numbers) if len(subset) > 0]

        for possible_tableau in list(powerset(subsets, self.permutation_group)):
            if len(possible_tableau) > 0:
                test_tableau = standard_tableau(possible_tableau)
                if test_tableau.permutation_group == self.permutation_group and test_tableau.check():
                        self.standard_tableaus.append(test_tableau)

        # # combine subsets into tableaus:
        # for i in range(1,self.permutation_group+1):
        #     for possible_tableau in list(itertools.combinations(subsets,i)):
        #         test_tableau = standard_tableau(possible_tableau)
        #         if test_tableau.permutation_group == self.permutation_group and test_tableau.check():
        #             self.standard_tableaus.append(test_tableau)
        #         else:
        #              print("wrong", possible_tableau)



    def calculate_all_overlap_integrals(self):
        pass

    def calculate_all_hamilton_integrals(self):
        pass

    def setup_matrix(self) -> str:
        pass


if __name__ == '__main__':
    p = permutation_group(4)
    p.get_all_standard_tableaus()

    for s in p.standard_tableaus:
        s.print()
        print()
