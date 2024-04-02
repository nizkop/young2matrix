from typing import List

from source.overview_pdf import overview_pdf
from source.standard_tableau import standard_tableau
from source.young_tableau import young_tableau


class permutation_group(object):
    def __init__(self):
        self.permutation_group: int = 0
        self.tableaus : List[young_tableau] = []
        self.standard_tableaus : List[standard_tableau] = []
        self.overview = overview_pdf()


    def print(self):
        pass

    def find_tableaus(self):
        pass

    def get_overview_pdf(self, title:str)->None:
        pass

    def get_all_standard_tableaus(self):
        pass

    def calculate_all_overlap_integrals(self):
        pass

    def calculate_all_hamilton_integrals(self):
        pass

    def setup_matrix(self) -> str:
        pass