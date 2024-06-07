from typing import List

from source.function_combination.calculate_hamilton_integral import calculate_hamilton_integral
from source.function_combination.calculate_overlap_integral import calculate_overlap_integral
from source.function_parts.get_dirac_notation import get_dirac_notation
from source.function_parts.HamiltonIntegral import HamiltonIntegral
from source.function_parts.SpinVsSpatialKind import SpinVsSpatialKind
from source.function_parts.TextKinds import TextKinds
from source.getting_subsets import get_powerset, permutations_of_subsets
from source.OverviewPdf import OverviewPdf
from source.ChemicalStandardTableau import ChemicalStandardTableau
from source.texts.general_texts import get_general_text
from source.texts.get_info_spin_possibilities import get_info_spin_possibilities
from source.texts.get_title_spatial import get_title_spatial
from source.texts.get_title_spin import get_title_spin
from source.texts.get_title_youngtableaus import get_title_multiplied_youngtableaus
from source.texts.get_titles_for_permutation_parts import get_title_permutation_to_tableaus
from source.YoungTableau import YoungTableau


class PermutationGroup(object):
    """
    todo
    """
    _instance = None # used as a singleton, limited to 1 instance at a time
    _instance_count = 0
    _max_instances = 1

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance_count >= cls._max_instances:
            raise ValueError("to many permutation_group instances (at the same time)")
        instance = super().__new__(cls)
        cls._instance_count += 1
        return instance
    def __del__(self):
        # print("__del",flush=True)
        type(self)._instance_count -= 1
        self._instance = None

    def __init__(self, permutation_group:int=0):
        self.permutation_group: int = permutation_group
        self.tableaus : List[YoungTableau] = []
        self.standard_tableaus : List[ChemicalStandardTableau] = []
        self.overview = OverviewPdf(permutation_group)

        self.overlap: List[dict] = []
        self.hamilton_integrals: List[HamiltonIntegral] = []

    def print(self) -> None:
       print(f"permutation group: S_{self.permutation_group}")
       for s in self.standard_tableaus:
           s.print()
           print()


    def get_young_tableau_equations(self) -> List[str]:
        """
        forming all tableaus into a latex equation,
        grouped by their outer shape and including the shortend/shape information (e.g. [1^2])
        :return: list of tex-formatted equations
        """
        equations = []
        self.get_all_standard_tableaus()
        for group in self.group_tableaus_by_shortend_symbol(tableaus_to_sort=self.standard_tableaus):
            equation = group[0].get_shortened_symbol()["tex"] + ":\quad"
            equation += r"\quad , \quad ".join([t.to_tex() for t in group])
            equations.append(equation)
        return equations

    def get_chapter_youngtableaus(self) -> None:
        """
        chapter 1 of overview giving pdf
        """
        self.overview.add_section(get_general_text("tableau_header"),
                                  content=get_title_permutation_to_tableaus(self.permutation_group))
        self.overview.vspace()
        for equation in self.get_young_tableau_equations():
            self.overview.add_latex_formula(equation)
            self.overview.vspace()
        self.overview.newpage()

    def get_chapter_multiplied(self) -> None:
        """
        chapter 2 of overview giving pdf
        """
        header, content = get_title_multiplied_youngtableaus(kind=TextKinds.TEX)
        self.overview.add_section(header,"")
        self.overview.add_section(get_general_text("spatial_header"), layer=1, content=content)
        for group in self.group_tableaus_by_shortend_symbol(tableaus_to_sort=self.standard_tableaus):
            self.overview.vspace()
            equation = group[0].get_shortened_symbol()["tex"] + ":"
            self.overview.add_latex_formula(equation)
            self.overview.vspace()
            for t in group:
                t.set_up_function()
                equation = t.to_tex() + "\quad " + t.function.to_tex()
                self.overview.add_latex_formula(equation)
                self.overview.vspace()
            self.overview.vspace()
        self.overview.newpage(False)

    def get_chapter_spinfunctions(self) -> None:
        """
        chapter 3 of overview giving pdf
        """
        self.overview.add_section(get_general_text("spin_header"), layer=1,
                                  content=get_info_spin_possibilities(self.permutation_group, kind=TextKinds.TEX))
        for group in self.group_tableaus_by_shortend_symbol(tableaus_to_sort=self.standard_tableaus):
            self.overview.vspace()
            equation = group[0].get_shortened_symbol()["tex"] + ":"
            self.overview.add_latex_formula(equation)
            self.overview.vspace()
            group_empty = True
            for t in group:
                tableau = t.to_tex()
                t.get_spin_choices()
                for s in t.spin_parts:
                    self.overview.add_latex_formula(tableau +r"\qquad "+ s.to_tex())
                    self.overview.vspace()
                    group_empty = False
            if group_empty:
                    self.overview.add_information(get_general_text("spin_2rows_tex"))

            self.overview.vspace()
        self.overview.newpage()

    def get_chapter_overlapintegrals(self) -> None:
        """
        chapter 4 of overview giving pdf
        """
        self.overview.add_section(get_general_text("header_overlap_general"), content="")
        title, content = get_title_spatial(kind=TextKinds.TEX)
        self.overview.add_section(sec_title=title, layer=1, content=content)
        self.calculate_all_overlap_integrals()
        for info in self.overlap:
            if info['kind'] == SpinVsSpatialKind.SPATIAL and len(info['result'].parts) == 1 and info['result'].parts[
                0].factor != 0 and info['result'].parts[0].factor != 1:
                equation_tex = get_dirac_notation(str(info['bra_tableau']), str(info['ket_tableau']),
                                                  kind=TextKinds.TEX)
                if info['kind'] == SpinVsSpatialKind.SPIN:
                    equation_tex += r"_{\sigma }"
                    equation_tex += "=" + get_dirac_notation(str(info['bra']), str(info['ket']), kind=TextKinds.TEX)
                equation_tex += r"_{\Phi}"
                equation_tex += f" = {info['result'].to_tex()}"
                self.overview.add_latex_formula(equation_tex)
                self.overview.vspace()

        self.overview.newpage(definitely=False)
        title, content, equation = get_title_spin(kind=TextKinds.TEX)
        self.overview.add_section(sec_title=title, layer=1, content=content)
        self.overview.add_latex_formula(equation)
        self.overview.vspace(), self.overview.vspace(), self.overview.vspace()
        for info in self.overlap:
            if info['kind'] == SpinVsSpatialKind.SPIN and len(info['result'].parts) == 1 and info['result'].parts[
                0].factor != 0 and info['result'].parts[0].factor != 1:
                equation_tex = get_dirac_notation(str(info['bra_tableau']), str(info['ket_tableau']),
                                                  kind=TextKinds.TEX)
                equation_tex += r"_{\sigma }"
                equation_tex += "=" + get_dirac_notation(str(info['bra']), str(info['ket']), kind=TextKinds.TEX)
                equation_tex += r"_{\Phi}"
                equation_tex += f" = {info['result'].to_tex()}"
                self.overview.add_latex_formula(equation_tex)
                self.overview.vspace()
        self.overview.newpage()

    def get_chapter_hamiltonintegrals(self) -> None:
        """
        chapter 5 of overview giving pdf
        """
        self.overview.add_section(get_general_text("header_hamilton_general"),"")
        self.overview.add_section(get_general_text("spatial_header"),content="",layer=1)
        self.overview.vspace()
        self.overview.vspace()
        self.calculate_all_hamilton_integrals()
        for info in self.hamilton_integrals:
            if len(info["hamilton_integral_sum"]) > 0:
                equation_tex = r"\bra{" + info["bra_tableau"] + r"}\hat{H}\ket{" + info["ket_tableau"] + r"}"
                if info["kind"] == SpinVsSpatialKind.SPATIAL.value:
                    equation_tex += r"_{\Phi}"
                equation_tex += " = "
                for addend in info["hamilton_integral_sum"]:
                    equation_tex += addend.to_tex()
            else:
                equation_tex = ""

            self.overview.add_latex_formula(equation_tex)
            self.overview.vspace()

        self.overview.newpage(definitely=False)
        self.overview.add_section(get_general_text("spin_header"),layer=1,
                                  content=get_general_text("h_info_spin")+get_general_text("ref_hspin"))

    def get_overview_pdf(self) -> None:
        """ creating a pdf with all calculated information about this particular permutation group """
        self.get_all_standard_tableaus()  # at least needed for chapter 4

        self.get_chapter_youngtableaus()
        self.get_chapter_multiplied()
        self.get_chapter_spinfunctions()
        self.get_chapter_overlapintegrals()
        self.get_chapter_hamiltonintegrals()

        self.overview.save()


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
                test_tableau = ChemicalStandardTableau(numbers_in_row=list(possible_tableau))
                if test_tableau.permutation_group == self.permutation_group and test_tableau.check():
                        self.standard_tableaus.append(test_tableau)

    def get_non_adjoint_tableaus(self) -> List[ChemicalStandardTableau]:
        """ choosing one orientation of tableaus (here: vertical alignment favored)
        e.g.: [1,2] adjoint to [1][2]
        :return: list of all tableaus, that are non-adjoint to others
        """
        if len(self.standard_tableaus) == 0:
            self.get_all_standard_tableaus()
        return [t for t in self.standard_tableaus if max(t.numbers_in_columns) <= t.number_of_rows]

    def group_tableaus_by_shortend_symbol(self, tableaus_to_sort:List[ChemicalStandardTableau]=[]) -> List[List[ChemicalStandardTableau]]:
        """
        sorting all tableaus by their outer shape (= same young tableau, different/same standard tableau)
        :return: 2d-list of grouped tableaus
        """
        if len(tableaus_to_sort) == 0:
            tableaus_to_sort = self.standard_tableaus
        tableaus = []
        for i in tableaus_to_sort:
            abbrevation = i.get_shortened_symbol()
            if len(tableaus) > 0 and tableaus[-1][-1].get_shortened_symbol()["plain_text"] == abbrevation["plain_text"]:
                tableaus[-1].append(i)
            else:
                tableaus.append([i])
        return tableaus


    def calculate_all_overlap_integrals(self) -> None:
        if len(self.overlap) > 0:
            return
        results = []
        for i in range(len(self.standard_tableaus)):
            tableau_1 = self.standard_tableaus[i]
            tableau_1.set_up_function()
            tableau_1.get_spatial_choices()
            tableau_1.get_spin_choices()
            tableau_1.calculate_all_overlap_integrals()
            for x in tableau_1.overlap:
                x["bra_tableau"] = tableau_1.to_tex()
                x["ket_tableau"] = tableau_1.to_tex()
                results.append(x)
            # mixed tableaus:
            for j in range(i+1, len(self.standard_tableaus)):
                tableau_2 = self.standard_tableaus[j]
                tableau_2.get_spatial_choices()
                tableau_2.get_spin_choices()

                results += calculate_overlap_integral(tableau_1, tableau_2, kind=SpinVsSpatialKind.SPATIAL)
                results += calculate_overlap_integral(tableau_1, tableau_2, kind=SpinVsSpatialKind.SPIN)

        for result in results:
            if result not in self.overlap:
                self.overlap.append(result)
        return

    def calculate_all_hamilton_integrals(self) -> None:
        """
        calculating the hamilton integrals between all tableaus of the group

        spin calculation is left out, because it reverts to overlap (because H is independent of spin)
        """
        for t in self.standard_tableaus:
            t.set_up_function()
            t.get_spatial_choices()
            t.get_spin_choices()

        self.calculate_all_hamilton_integrals_kind()#only spatial

    def calculate_all_hamilton_integrals_kind(self) -> None:
        """
        finding all combinations for hamilton integrals
        -> also between identical tableaus,
        only hamilton integrals between different young tableaus (!= standard) are set to 0);
        saving results in self.hamilton_integrals
        """
        # Tableaus need to be set up already !
        if len(self.hamilton_integrals) > 0:
            return
        results = []
        for i in range(len(self.standard_tableaus)):
            tableau_1 = self.standard_tableaus[i]
            for j in range(i, len(self.standard_tableaus)):
                info = {}
                tableau_2 = self.standard_tableaus[j]
                info["bra_tableau"] = tableau_1.to_tex()
                info["ket_tableau"] = tableau_2.to_tex()
                info["kind"] = SpinVsSpatialKind.SPATIAL.value
                info["hamilton_integral_sum"] = calculate_hamilton_integral(tableau_1, tableau_2, kind=SpinVsSpatialKind.SPATIAL)
                if len(info["hamilton_integral_sum"]) > 0:
                    results.append(info)
        added = []
        for result in results:
            if sorted([result["bra_tableau"], result["ket_tableau"]]) not in added:
                self.hamilton_integrals.append(result)
                added.append(sorted([result["bra_tableau"], result["ket_tableau"]]))
        return

    def setup_matrix(self) -> str:
        pass

