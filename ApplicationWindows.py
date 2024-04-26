
import sys
import time
from typing import Union
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QLabel,QLineEdit, QMessageBox, QSizePolicy


from MainApplication import MainApplication
from source.function_parts.get_dirac_notation import get_dirac_notation
from source.function_parts.spin_vs_spatial_kind import spin_vs_spatial_kind
from source.function_parts.text_kinds import text_kinds
from source.permutation_group import permutation_group
from source.texts.general_texts import general_texts
from source.texts.get_title_spatial import get_title_spatial
from source.texts.get_title_spin import get_title_spin
from source.texts.get_title_youngtableaus import get_title_multiplied_youngtableaus


class ApplicationWindows(MainApplication):

    def __init__(self):
        super().__init__()

        # self.pages = [
        #     {"name": "Startseite", "sign": "zurück zum Start", "index": 0, "function": self.load_main_page},
        #     {"name": "Tableaus", "sign": "[1][2]", "index": 1, "function": self.load_tableau_page},
        #     {"name": "Spin","sign": "σ", "index": 3, "function": self.load_spin_page},
        #     {"name": "Raumfunktionen", "sign": "Φ", "index": 3, "function": self.load_spatial_page},
        #     {"name": "Download", "sign": "⬇️", "index": 4, "function": self.test_page}
        # ]
        self.permutation_group: Union[None, permutation_group] = None
        self.permutation_group_no: Union[None, int] = None


    def open_page(self, page_number:int):
        """ checking the input and (if the input is okay) loading another page """
        print("open_page:", page_number)
        # getting and checking the input information:
        if page_number == 0:
            return self.change_page(page_number)
        if self.current_page == 0:
            input_value = self.input_box.text()
            if not input_value:
                QMessageBox.warning(self, "Warnung", general_texts["warning_no_group"])
                return self.change_page(0)
            try:
                input_value = int(input_value)
                if input_value <= 0:
                    QMessageBox.warning(self, "Warnung", general_texts["warning_wrong_number"])
                    return self.change_page(0)
            except:
                QMessageBox.warning(self, "Warnung", general_texts["warning_wrong_type"])
                return self.change_page(0)
            self.set_basic_permutation_attributes(input_value=input_value)
        self.change_page(page_number)


    def set_basic_permutation_attributes(self, input_value:int):
        if (self.permutation_group_no is not None and self.permutation_group is not None and
                self.permutation_group_no == input_value and self.permutation_group.permutation_group == input_value):
            return
        self.permutation_group_no = input_value
        self.permutation_group = permutation_group(self.permutation_group_no)


    def update_page(self):
        """ adding content to layout """
        print("update page Windows:", self.current_page)
        # if self.current_page == 1:
        #     return self.load_tableau_page()
        # elif self.current_page == 3:
        #     return self.test_page()
        # self.current_page = 0
        # self.load_main_page()

        # else:
        try:
            page_info = next((page_dict for page_dict in self.pages if page_dict.get("index") == self.current_page), None)
            page_info["function"]()
        except KeyError:
            self.current_page = 0
            return self.load_main_page()

    def test_page(self):
        # working equations:
        eqs = [r"E = m \cdot c^ 2", r"\frac{1}{2}", "\\begin{array}{c}{1}\\end{array}", r"\begin{array}{|c|}{2}\end{array}",
               "\\bra{1}"]  # "\\text{a}"]
        for eq in eqs:
            self.add_equation(formula=eq)


    def load_tableau_page(self):
        # page_info = next((page_dict for page_dict in self.pages if page_dict.get("index") == self.current_page), None)
        self.permutation_group.get_all_standard_tableaus()
        for equation in self.permutation_group.get_young_tableau_equations():
            self.add_equation(formula=equation)

    def load_spin_page(self):
        self.permutation_group.get_all_standard_tableaus()
        for group in self.permutation_group.group_tableaus_by_shortend_symbol(tableaus_to_sort=self.permutation_group.standard_tableaus):
            equation = group[0].get_shortend_symbol()["tex"] + ":"
            self.add_equation(equation)
            group_empty = True
            for t in group:
                tableau = t.to_tex()
                t.get_spin_choices()
                for s in t.spin_parts:
                    self.add_equation(tableau +r"\qquad "+ s.to_tex())
                    group_empty = False
            if group_empty:
                label = QLabel(general_texts["spin_2rows"])
                self.scroll_layout.addWidget(label)
                self.non_basics.append(label)



    def load_spatial_page(self):
        self.permutation_group.get_all_standard_tableaus()
        for group in self.permutation_group.group_tableaus_by_shortend_symbol(
                tableaus_to_sort=self.permutation_group.standard_tableaus):
            equation = group[0].get_shortend_symbol()["tex"] + ":"
            self.add_equation(equation)
            group_empty = True
            for t in group:
                tableau = t.to_tex()
                t.get_spatial_choices()
                for s in t.spatial_parts:
                    self.add_equation(tableau + r"\qquad " + s.to_tex())
                    group_empty = False
            if group_empty:
                label = QLabel(general_texts["spatial_2columns"])
                self.scroll_layout.addWidget(label)
                self.non_basics.append(label)

    def load_tableau_page_multiplied(self):
        label = QLabel(":\n".join(get_title_multiplied_youngtableaus(kind=text_kinds.TXT)))
        self.scroll_layout.addWidget(label)
        self.non_basics.append(label)
        for group in self.permutation_group.group_tableaus_by_shortend_symbol(tableaus_to_sort=self.permutation_group.standard_tableaus):
            equation = group[0].get_shortend_symbol()["tex"] + ":"
            self.add_equation(equation)
            for t in group:
                t.set_up_function()
                equation = t.to_tex() + "\quad " + t.function.to_tex()
                self.add_equation(equation)


    def load_main_page(self):
        permutation_group_input = QHBoxLayout()
        permutation_group_label = QLabel(general_texts["input_command"])
        permutation_group_input.addWidget(permutation_group_label)
        self.input_box = QLineEdit()
        permutation_group_input.addWidget(self.input_box)

        # spacer to center input line
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        permutation_group_input.addWidget(spacer)

        self.scroll_layout.addLayout(permutation_group_input)
        self.scroll_layout.setStretch(self.scroll_layout.indexOf(spacer),1)

        self.non_basics.append(permutation_group_label)
        self.non_basics.append(permutation_group_input)
        self.non_basics.append(self.input_box)


    def load_download(self):
        """ initializes download and goes back to main page """
        try:
            self.permutation_group.get_overview_pdf()
            label = QLabel(general_texts["successful_download"])
            self.scroll_layout.addWidget(label)
            self.non_basics.append(label)
        except:
            label = QLabel(general_texts["failed_download"])
            self.scroll_layout.addWidget(label)
            self.non_basics.append(label)

        time.sleep(5)
        # reset
        self.permutation_group_no = None
        self.open_page(0)


    def load_overlap_spin(self):
        title, content, equation = get_title_spin(kind=text_kinds.TXT)
        label = QLabel(title + "\n" + content)
        self.scroll_layout.addWidget(label)
        self.non_basics.append(label)
        self.add_equation(equation)
        for i in self.permutation_group.overlap:
            if i['kind'] == spin_vs_spatial_kind.SPIN and len(i['result'].parts) == 1 and i['result'].parts[
                0].factor != 0 and i['result'].parts[0].factor != 1:
                equation_tex = get_dirac_notation(str(i['bra_tableau']), str(i['ket_tableau']), kind=text_kinds.TEX)
                equation_tex += r"_{\sigma }"
                equation_tex += "=" + get_dirac_notation(str(i['bra']), str(i['ket']), kind=text_kinds.TEX)
                equation_tex += r"_{\Phi}"
                equation_tex += f" = {i['result'].to_tex()}"
                self.add_equation(equation_tex)

    def load_overlap_spatial(self):
        title, content = get_title_spatial(kind=text_kinds.TXT)
        label = QLabel(title+"\n"+content)
        self.scroll_layout.addWidget(label)
        self.non_basics.append(label)
        self.permutation_group.calculate_all_overlap_integrals()
        for i in self.permutation_group.overlap:
            if i['kind'] == spin_vs_spatial_kind.SPATIAL and len(i['result'].parts) == 1 and i['result'].parts[
                0].factor != 0 and i['result'].parts[0].factor != 1:
                equation_tex = get_dirac_notation(str(i['bra_tableau']), str(i['ket_tableau']), kind=text_kinds.TEX)
                if i['kind'] == spin_vs_spatial_kind.SPIN:
                    equation_tex += r"_{\sigma }"
                    equation_tex += "=" + get_dirac_notation(str(i['bra']), str(i['ket']), kind=text_kinds.TEX)
                equation_tex += r"_{\Phi}"
                equation_tex += f" = {i['result'].to_tex()}"
                self.add_equation(equation_tex)















if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindows()
    window.show()
    sys.exit(app.exec_())
