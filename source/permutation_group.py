from typing import List

from source.function_combination.calculate_hamilton_integral import calculate_hamilton_integral
from source.function_combination.calculate_overlap_integral import calculate_overlap_integral
from source.function_parts.get_dirac_notation import get_dirac_notation
from source.function_parts.hamilton_integral import hamilton_integral
from source.function_parts.spin_vs_spatial_kind import spin_vs_spatial_kind
from source.function_parts.text_kinds import text_kinds
from source.getting_subsets import get_powerset, permutations_of_subsets
from source.overview_pdf import overview_pdf
from source.chemical_standard_tableau import chemical_standard_tableau
from source.texts.general_texts import get_general_text
from source.texts.get_info_spin_possibilities import get_info_spin_possibilities
from source.texts.get_title_spatial import get_title_spatial
from source.texts.get_title_spin import get_title_spin
from source.texts.get_title_youngtableaus import get_title_multiplied_youngtableaus
from source.texts.get_titles_for_permutation_parts import get_title_permutation_to_tableaus
from source.young_tableau import young_tableau


class permutation_group(object):
    def __init__(self, permutation_group:int=0):
        self.permutation_group: int = permutation_group
        self.tableaus : List[young_tableau] = []
        self.standard_tableaus : List[chemical_standard_tableau] = []
        self.overview = overview_pdf()
        self.title_pdf = f"group_{self.permutation_group}"

        self.overlap: List[dict] = []
        self.hamiltonians: List[hamilton_integral] = []

    def print(self) -> None:
       print(f"permutation group: S_{self.permutation_group}")
       for s in self.standard_tableaus:
           s.print()
           print()


    def get_young_tableau_equations(self) -> List[str]:
        equations = []
        self.get_all_standard_tableaus()
        for group in self.group_tableaus_by_shortend_symbol(tableaus_to_sort=self.standard_tableaus):
            equation = group[0].get_shortend_symbol()["tex"]+ ":\quad"
            equation += r"\quad , \quad ".join([t.to_tex() for t in group])
            equations.append(equation)
        return equations


    def get_chapter_youngtableaus(self):
        """
        chapter 1 of overview giving pdf
        """
        self.overview.add_section("Young-Tableaus",
                                  content=get_title_permutation_to_tableaus(self.permutation_group))
        self.overview.vspace()
        for equation in self.get_young_tableau_equations():
            self.overview.add_latex_formula(equation)
            self.overview.vspace()
        self.overview.newpage()

    def get_chapter_multiplied(self):
        """
        chapter 2 of overview giving pdf
        """
        header, content = get_title_multiplied_youngtableaus(kind=text_kinds.TEX)
        self.overview.add_section(header, content=content)
        for group in self.group_tableaus_by_shortend_symbol(tableaus_to_sort=self.standard_tableaus):
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

    def get_chapter_spinfunctions(self):
        """
        chapter 3 of overview giving pdf
        """
        self.overview.add_section("Spin",content=get_info_spin_possibilities(self.permutation_group, kind=text_kinds.TEX))
        for group in self.group_tableaus_by_shortend_symbol(tableaus_to_sort=self.standard_tableaus):
            self.overview.vspace()
            equation = group[0].get_shortend_symbol()["tex"] + ":"
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

    def get_chapter_overlapintegrals(self):
        """
        chapter 4 of overview giving pdf
        """
        self.overview.add_section("Überlappungsintegrale", content="")
        title, content = get_title_spatial(kind=text_kinds.TEX)
        self.overview.add_section(sec_title=title, layer=1, content=content)
        self.calculate_all_overlap_integrals()
        for info in self.overlap:
            if info['kind'] == spin_vs_spatial_kind.SPATIAL and len(info['result'].parts) == 1 and info['result'].parts[
                0].factor != 0 and info['result'].parts[0].factor != 1:
                equation_tex = get_dirac_notation(str(info['bra_tableau']), str(info['ket_tableau']),
                                                  kind=text_kinds.TEX)
                if info['kind'] == spin_vs_spatial_kind.SPIN:
                    equation_tex += r"_{\sigma }"
                    equation_tex += "=" + get_dirac_notation(str(info['bra']), str(info['ket']), kind=text_kinds.TEX)
                equation_tex += r"_{\Phi}"
                equation_tex += f" = {info['result'].to_tex()}"
                self.overview.add_latex_formula(equation_tex)
                self.overview.vspace()

        self.overview.newpage()
        title, content, equation = get_title_spin(kind=text_kinds.TEX)
        self.overview.add_section(sec_title=title, layer=1, content=content)
        self.overview.add_latex_formula(equation)
        self.overview.vspace(), self.overview.vspace(), self.overview.vspace()
        for info in self.overlap:
            if info['kind'] == spin_vs_spatial_kind.SPIN and len(info['result'].parts) == 1 and info['result'].parts[
                0].factor != 0 and info['result'].parts[0].factor != 1:
                equation_tex = get_dirac_notation(str(info['bra_tableau']), str(info['ket_tableau']),
                                                  kind=text_kinds.TEX)
                equation_tex += r"_{\sigma }"
                equation_tex += "=" + get_dirac_notation(str(info['bra']), str(info['ket']), kind=text_kinds.TEX)
                equation_tex += r"_{\Phi}"
                equation_tex += f" = {info['result'].to_tex()}"
                self.overview.add_latex_formula(equation_tex)
                self.overview.vspace()

    def get_chapter_hamiltonintegrals(self):
        """
        chapter 5 of overview giving pdf
        """
        self.overview.add_section("Hamiltonmatrixelemente",
                                  content=get_general_text("h_info_spin"))
        self.calculate_all_hamilton_integrals()
        for info in self.hamiltonians:
            if len(info["hamilton_integral_sum"]) > 0:
                equation_tex = r"\bra{" + info["bra_tableau"] + r"}\hat{H}\ket{" + info["ket_tableau"] + r"}"
                if info["kind"] == spin_vs_spatial_kind.SPATIAL.value:
                    equation_tex += r"_{\Phi}"
                equation_tex += " = "
                for addend in info["hamilton_integral_sum"]:
                    equation_tex += addend.to_tex()

            self.overview.add_latex_formula(equation_tex)
            self.overview.vspace()

    def get_overview_pdf(self) -> None:
        """ creating a pdf with all calculated information about this particular permutation group """
        self.get_all_standard_tableaus()  # at least needed for chapter 4

        self.get_chapter_youngtableaus()
        self.get_chapter_multiplied()
        self.get_chapter_spinfunctions()
        self.get_chapter_overlapintegrals()
        self.get_chapter_hamiltonintegrals()

        self.overview.save(title=self.title_pdf)


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
        return [t for t in self.standard_tableaus if max(t.numbers_in_columns) <= t.number_of_rows]

    def group_tableaus_by_shortend_symbol(self, tableaus_to_sort:List[chemical_standard_tableau]=[]) -> List[List[chemical_standard_tableau]]:
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


    def calculate_all_overlap_integrals(self) -> None:
        if len(self.overlap) > 0:
            return
        results = []
        for i in range(len(self.standard_tableaus)):
            tableau_1 = self.standard_tableaus[i]
            tableau_1.set_up_function()
            tableau_1.get_spatial_choices()
            tableau_1.get_spin_choices()
            tableau_1.calulate_all_overlap_integrals()
            for x in tableau_1.overlap:
                x["bra_tableau"] = tableau_1.to_tex()
                x["ket_tableau"] = tableau_1.to_tex()
                results.append(x)
            # mixed tableaus:
            for j in range(i+1, len(self.standard_tableaus)):
                tableau_2 = self.standard_tableaus[j]
                tableau_2.get_spatial_choices()
                tableau_2.get_spin_choices()

                results += calculate_overlap_integral(tableau_1, tableau_2, kind=spin_vs_spatial_kind.SPATIAL)
                results += calculate_overlap_integral(tableau_1, tableau_2, kind=spin_vs_spatial_kind.SPIN)

        for result in results:
            if result not in self.overlap:
                self.overlap.append(result)
        return

    def calculate_all_hamilton_integrals(self):
        for t in self.standard_tableaus:
            t.set_up_function()
            t.get_spatial_choices()
            t.get_spin_choices()

        self.calculate_all_hamilton_integrals_kind(spin_vs_spatial_kind.SPATIAL)
        # self.calculate_all_hamilton_integrals_kind(spin_vs_spatial_kind.SPIN)# TODO spin : reverts to overlap, because H is independend of spin!!!

    def calculate_all_hamilton_integrals_kind(self, kind: spin_vs_spatial_kind):
        # Tableaus need to be set up already !
        if len([x for x in self.hamiltonians if x["kind"] == kind.value]) > 0:
            return
        results = []
        for i in range(len(self.standard_tableaus)):
            tableau_1 = self.standard_tableaus[i]
            for j in range(i, len(self.standard_tableaus)):
                info = {}
                tableau_2 = self.standard_tableaus[j]
                info["bra_tableau"] = tableau_1.to_tex()
                info["ket_tableau"] = tableau_2.to_tex()
                info["kind"] = kind.value
                info["hamilton_integral_sum"] = calculate_hamilton_integral(tableau_1, tableau_2, kind=kind)

                if len(info["hamilton_integral_sum"]) > 0:
                    results.append(info)

        added = []
        for result in results:
            if sorted([result["bra_tableau"], result["ket_tableau"]]) not in added:
                self.hamiltonians.append(result)
                added.append(sorted([result["bra_tableau"], result["ket_tableau"]]))
        return

    def setup_matrix(self) -> str:
        pass


if __name__ == '__main__':
    p = permutation_group(3)
    p.get_all_standard_tableaus()
    # p.print()

    # results = p.calculate_all_overlap_integrals()
    # for i in results:
    #     print(f"<{i['bra']}|{i['ket']}> = {i['result'].to_tex()}")


    p.get_overview_pdf()
