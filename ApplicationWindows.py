
import sys
from typing import Union
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QLabel,QLineEdit, QMessageBox, QSizePolicy


from MainApplication import MainApplication
from source.permutation_group import permutation_group


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
        # getting and checking the input information:
        if page_number == 0:
            return self.change_page(page_number)
        input_value = self.input_box.text()
        if not input_value:
            QMessageBox.warning(self, "Warnung", "Bitte geben Sie eine Permutationsgruppe ein.")
            return self.change_page(0)
        try:
            input_value = int(input_value)
            if input_value <= 0:
                QMessageBox.warning(self, "Warnung", "Bitte geben Sie eine Permutationsgruppe als positive Zahl.")
                return self.change_page(0)
        except:
            QMessageBox.warning(self, "Warnung", "Bitte geben Sie die Nummer für eine Permutationsgruppe ein.")
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
        print("groups:", len(self.permutation_group.group_tableaus_by_shortend_symbol(tableaus_to_sort=self.permutation_group.standard_tableaus)))
        for group in self.permutation_group.group_tableaus_by_shortend_symbol(tableaus_to_sort=self.permutation_group.standard_tableaus):
            equation = group[0].get_shortend_symbol()["tex"] + ":"
            self.add_equation(equation)
            group_empty = True
            print("t:", len(group))
            for t in group:
                tableau = t.to_tex()
                t.get_spin_choices()
                for s in t.spin_parts:
                    self.add_equation(tableau +r"\qquad "+ s.to_tex())
                    group_empty = False
            # if group_empty:
            #         add_information(r"\textit{(Da es nur zwei Spinfunktionen $\alpha, \beta$ gibt, sind mehr als zwei antisymmetrische Funktionen nicht möglich.)}")


    def load_spatial_page(self):
        pass


    def load_main_page(self):
        permutation_group_input = QHBoxLayout()
        permutation_group_label = QLabel("Permutationsgruppe:")
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












if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindows()
    window.show()
    sys.exit(app.exec_())
