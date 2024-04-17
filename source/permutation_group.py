from typing import List

from source.getting_subsets import get_powerset, permutations_of_subsets
from source.overview_pdf import overview_pdf
from source.chemical_standard_tableau import chemical_standard_tableau
from source.texts.get_info_spin_possibilities import get_info_spin_possibilities
from source.texts.get_titles_for_permutation_parts import get_title_permutation_to_tableaus
from source.young_tableau import young_tableau


class permutation_group(object):
    def __init__(self, permutation_group:int=0):
        self.permutation_group: int = permutation_group
        self.tableaus : List[young_tableau] = []
        self.standard_tableaus : List[chemical_standard_tableau] = []
        self.overview = overview_pdf()

    def print(self) -> None:
       print(f"permutation group: S_{self.permutation_group}")
       for s in self.standard_tableaus:
           s.print()
           print()

    def find_tableaus(self):
        pass


    def get_young_tableau_equations(self) -> List[str]:
        equations = []
        self.get_all_standard_tableaus()
        for group in self.group_tableaus_by_shortend_symbol(tableaus_to_sort=p.standard_tableaus):
            equation = group[0].get_shortend_symbol()["tex"]+ ":\quad"
            equation += r"\quad , \quad ".join([t.to_tex() for t in group])
            equations.append(equation)
        return equations

    def get_overview_pdf(self) -> None:
        """ creating a pdf with all calculated information about this particular permutation group """
        title = f"group_{self.permutation_group}"

        # page 1
        self.overview.add_section("Young-Tableaus",
                                  content=get_title_permutation_to_tableaus(self.permutation_group))
        self.overview.vspace()
        for equation in self.get_young_tableau_equations():
            self.overview.add_latex_formula(equation)
            self.overview.vspace()
        self.overview.newpage()

        # page 2
        self.overview.add_section("Ausmultiplizierte Young-Tableaus",
                                  content=r"$a, b, c, \hdots \quad $ = allgemeine Funktionen, "+
                                          r"die beispielsweise p-Orbitale repräsentieren könnten")
        for group in self.group_tableaus_by_shortend_symbol(tableaus_to_sort=p.standard_tableaus):
            self.overview.vspace()
            equation = group[0].get_shortend_symbol()["tex"] + ":"
            self.overview.add_latex_formula(equation)
            self.overview.vspace()
            for t in group:
                t.set_up_function()
                equation = t.to_tex() + "\quad " + t.function.to_tex()
                self.overview.add_latex_formula(equation)
                self.overview.vspace()
            self.overview.vspace()
        self.overview.newpage()

        # page 3
        self.overview.add_section("Spin",content=get_info_spin_possibilities(self.permutation_group))
        for group in self.group_tableaus_by_shortend_symbol(tableaus_to_sort=p.standard_tableaus):
            self.overview.vspace()
            equation = group[0].get_shortend_symbol()["tex"] + ":"
            self.overview.add_latex_formula(equation)
            self.overview.vspace()
            for t in group:
                tableau = t.to_tex()
                t.get_spin_choices()
                for s in t.spin_parts:
                    self.overview.add_latex_formula(tableau +r"\qquad "+ s.to_tex())
                    self.overview.vspace()
            self.overview.vspace()
        self.overview.newpage()

        self.overview.save(title=title)


    def get_all_standard_tableaus(self) -> None:
        """
        creating all possible young (standard) tableaus from the number of the permutation group
        :return: None, because result is written into self.standard_tableaus
        """
        # print("get_all_standard_tableaus", flush=True)
        if len(self.standard_tableaus) > 0:
            # duplicate calculations are adding redundant tableaus
            # and re-calculation takes up more ressources
            return
        # find subsets of all combinations:
        numbers = list(range(1, self.permutation_group + 1))
        subsets = [subset for subset in get_powerset(array=numbers) if len(subset) > 0]

        # combine subsets into tableaus:
        for possible_tableau in list(permutations_of_subsets(array=subsets, group_number=self.permutation_group)):
            if len(possible_tableau) > 0:
                test_tableau = chemical_standard_tableau(numbers_in_row=list(possible_tableau))
                if test_tableau.permutation_group == self.permutation_group and test_tableau.check():
                        self.standard_tableaus.append(test_tableau)

    def get_non_adjoint_tableaus(self) -> List[chemical_standard_tableau]:
        """ choosing one orientation of tableaus (here: vertical alignment favored)
        e.g.: [1,2] adjoint to [1][2]
        """
        if len(self.standard_tableaus) == 0:
            self.get_all_standard_tableaus()
        return [t for t in self.standard_tableaus if max(t.number_of_columns) <= t.number_of_rows]

    def group_tableaus_by_shortend_symbol(self, tableaus_to_sort:List[chemical_standard_tableau]=[]):
        if len(tableaus_to_sort) == 0:
            tableaus_to_sort = self.standard_tableaus
        tableaus = []
        for i in tableaus_to_sort:
            abbrevation = i.get_shortend_symbol()
            if len(tableaus) > 0 and tableaus[-1][-1].get_shortend_symbol()["plain_text"] == abbrevation["plain_text"]:
                tableaus[-1].append(i)
            else:
                tableaus.append([i])
        return tableaus


    def calculate_all_overlap_integrals(self):
        pass

    def calculate_all_hamilton_integrals(self):
        pass

    def setup_matrix(self) -> str:
        pass


if __name__ == '__main__':
    p = permutation_group(2)
    p.get_all_standard_tableaus()
    # p.print()

    p.get_overview_pdf()
