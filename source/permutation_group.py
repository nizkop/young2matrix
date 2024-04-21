from typing import List, Union

from source.function_combination import function_combination
from source.function_parts.get_dirac_notation import get_dirac_notation
from source.function_parts.spin_vs_spatial_kind import spin_vs_spatial_kind
from source.function_parts.ttext_kinds import text_kinds
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

        self.overlap: List[dict] = []

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
        self.get_all_standard_tableaus() #at least needed for chapter 4

        # chapter 1
        self.overview.add_section("Young-Tableaus",
                                  content=get_title_permutation_to_tableaus(self.permutation_group))
        self.overview.vspace()
        for equation in self.get_young_tableau_equations():
            self.overview.add_latex_formula(equation)
            self.overview.vspace()
        self.overview.newpage()

        # chapter 2 # TODO: ensure line break for long eq
        self.overview.add_section("Ausmultiplizierte Young-Tableaus",
                                  content=r"$a, b, c, \hdots \quad $ = allgemeine Funktionen, "+
                                          r"die beispielsweise p-Orbitale repräsentieren könnten")
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

        # chapter 3
        self.overview.add_section("Spin",content=get_info_spin_possibilities(self.permutation_group))
        for group in self.group_tableaus_by_shortend_symbol(tableaus_to_sort=self.standard_tableaus):
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

        # chapter 4
        self.overview.add_section("Überlappungsintegrale",
                                  content=r"Raumfunktionen:\\"+
                                          r" (nur nicht verschwindende Kombinationen gezeigt)\\"
                                          r"identische Tableaus ergeben (aufgrund der normierten Funktionen darin) automatisch 1 und werden daher hier nicht aufgelistet")
        self.calculate_all_overlap_integrals(kind=spin_vs_spatial_kind.SPATIAL)
        for i in self.overlap:
            if i['kind'] == spin_vs_spatial_kind.SPATIAL and len(i['result'].parts) == 1 and i['result'].parts[0].factor != 0 and i['result'].parts[0].factor != 1:
            # if len(i['result'].parts) == 1 and i['result'].parts[0].factor != 0 and i['result'].parts[0].factor != 1:
                equation_tex = get_dirac_notation(str(i['bra_tableau']), str(i['ket_tableau']), kind=text_kinds.TEX)
                if i['kind'] == spin_vs_spatial_kind.SPIN:
                    equation_tex += r"_{\sigma }"
                    equation_tex += "=" + get_dirac_notation(str(i['bra']), str(i['ket']), kind=text_kinds.TEX)
                # elif i['kind'] == spin_vs_spatial_kind.SPATIAL:
                equation_tex += r"_{\Phi}"
                # equation_tex += "=" + get_dirac_notation(str(i['bra']), str(i['ket']), kind=text_kinds.TEX)
                equation_tex += f" = {i['result'].to_tex()}"
                self.overview.add_latex_formula(equation_tex)
                self.overview.vspace()

        self.overview.newpage()
        self.overview.add_information(r"Spinfunktionen:\\ (nur nicht verschwindende Kombinationen gezeigt) \\ "+
                                      r"Überlapp zw. versch. Tableaus ist 0, "+
                                      r"Überlapp zwischen gleichen Tableaus mit gleichem $m_S$-Wert ist 1\\"+
                                      r"hier informale Darstellung der Tableaus mit Spinfunktionen nach dem Schema: "
                                      )
        self.overview.add_latex_formula(r"\bra{\,\text{Tableau 1}\,}\ket{\,\text{Tableau 2}\,} "+
                                        r"= \bra{\, \underbrace{S \quad m_S}_{\text{von Tableau 1}} \,}"+
                                        r" \ket{\, \underbrace{S \quad m_S}_{\text{von Tableau 2}} \,} "+
                                        r"= \underbrace{...}_{\text{Überlapp der Tableaus 1 und 2}}")
        self.overview.vspace(), self.overview.vspace(), self.overview.vspace()
        self.calculate_all_overlap_integrals(kind=spin_vs_spatial_kind.SPATIAL)
        for i in self.overlap:
            if i['kind'] == spin_vs_spatial_kind.SPIN and len(i['result'].parts) == 1 and i['result'].parts[0].factor != 0:
            # if len(i['result'].parts) == 1 and i['result'].parts[0].factor != 0 and i['result'].parts[0].factor != 1:
                equation_tex = get_dirac_notation(str(i['bra_tableau']), str(i['ket_tableau']), kind=text_kinds.TEX)
                equation_tex += r"_{\sigma }"
                equation_tex += "=" + get_dirac_notation(str(i['bra']), str(i['ket']), kind=text_kinds.TEX)
                # elif i['kind'] == spin_vs_spatial_kind.SPATIAL:
                equation_tex += r"_{\Phi}"
                # equation_tex += "=" + get_dirac_notation(str(i['bra']), str(i['ket']), kind=text_kinds.TEX)
                equation_tex += f" = {i['result'].to_tex()}"
                self.overview.add_latex_formula(equation_tex)
                self.overview.vspace()

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


    def calculate_all_overlap_integrals(self, kind: spin_vs_spatial_kind):
        # TODO: check
        results = []
        for i in range(len(self.standard_tableaus)):
            tableau_1 = self.standard_tableaus[i]
            # tableau_1.set_up_function()
            # tableau_1.get_spatial_choices()
            # tableau_1.get_spin_choices()
            tableau_1.calulate_all_overlap_integrals()
            for x in tableau_1.overlap:
                x["bra_tableau"] = tableau_1.to_tex()
                x["ket_tableau"] = tableau_1.to_tex()
                results.append(x)

            # mixed tableaus:
            for j in range(i+1, len(self.standard_tableaus)):
                # should anyway be 0
                tableau_2 = self.standard_tableaus[j]
                tableau_2.get_spatial_choices()
                tableau_2.get_spin_choices()
                f = function_combination(tableau_1,tableau_2)
                info = {"bra_tableau": tableau_1.to_tex(), "ket_tableau": tableau_2.to_tex(),
                        "kind": kind}
                if kind == spin_vs_spatial_kind.SPIN:
                    # multiple results
                    for sp in range(len(tableau_1.spin_parts)):
                        spin_choice = tableau_1.spin_parts[sp]
                        for sp2 in range(sp, len(tableau_2.spin_parts)):
                            spin_choice_2 = tableau_2.spin_parts[sp2]
                            g = f.calculate_overlap_integral_between_functions(spin_choice.function, spin_choice_2.function)
                            info["bra"] = spin_choice.to_tex()
                            info["ket"] = spin_choice_2.to_tex()
                            info["result"] = g
                            results.append(info)
                else:
                    if kind == spin_vs_spatial_kind.GENERAL:
                        g = f.calculate_overlap_integral_basisfunction()
                        info["bra"] = tableau_1.function.to_tex()
                        info["ket"] = tableau_2.function.to_tex()
                    elif kind == spin_vs_spatial_kind.SPATIAL:
                        if len(tableau_1.spatial_parts) > 0 and len(tableau_2.spatial_parts) > 0:
                            # assumption that only 1 part per tableau
                            g = f.calculate_overlap_integral_between_functions(tableau_1.spatial_parts[0].function, tableau_2.spatial_parts[0].function)
                            info["bra"] = tableau_1.spatial_parts[0].function
                            info["ket"] = tableau_2.spatial_parts[0].function
                        else:
                            continue
                    info["result"] = g
                    results.append(info)

        for result in results:
            if result not in self.overlap:
                self.overlap.append(result)
        return

    def calculate_all_hamilton_integrals(self):
        pass

    def setup_matrix(self) -> str:
        pass


if __name__ == '__main__':
    p = permutation_group(4)
    p.get_all_standard_tableaus()
    # p.print()

    # results = p.calculate_all_overlap_integrals()
    # for i in results:
    #     print(f"<{i['bra']}|{i['ket']}> = {i['result'].to_tex()}")


    p.get_overview_pdf()
