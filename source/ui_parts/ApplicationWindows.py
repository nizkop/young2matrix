
import sys
from typing import Union
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox, QSizePolicy, \
    QProgressBar, QPushButton, QWidgetItem, QLayoutItem, QVBoxLayout

from source.function_parts.get_dirac_notation import get_dirac_notation
from source.function_parts.spin_vs_spatial_kind import spin_vs_spatial_kind
from source.function_parts.text_kinds import text_kinds
from source.permutation_group import permutation_group
from source.texts.general_texts import get_general_text
from source.texts.get_title_spatial import get_title_spatial
from source.texts.get_title_spin import get_title_spin
from source.texts.get_title_youngtableaus import get_title_multiplied_youngtableaus
from source.ui_parts.MainApplication import MainApplication
from source.ui_parts.DownloadThread import DownloadThread
from source.ui_parts.settings.idea_config import get_language


class ApplicationWindows(MainApplication):
    """
    class needed to fill ui pages of main application with actual content
    """

    def __init__(self):
        super().__init__()

        self.permutation_group: Union[None, permutation_group] = None
        self.permutation_group_no: Union[None, int] = None


    def open_page(self, page_number:int) -> None:
        """ checking the input and (if the input is okay) loading another page """
        print("open_page:", page_number)
        # getting and checking the input information:
        if page_number == 0:
            return self.change_page(page_number)
        warning_text = None
        if self.current_page == 0:
            input_value = self.input_box.text()
            if not input_value:
                warning_text = get_general_text("warning_no_group")
            try:
                input_value = int(input_value)
                if input_value <= 0:
                    warning_text = get_general_text("warning_wrong_number")
                elif input_value >= 10:
                    # double check before calculating too much (because high numbers might fry the computer)
                    warning_box = QMessageBox()
                    warning_box.setText(get_general_text("check_big_data"))
                    warning_box.setStyleSheet(f"color: black; background-color: {self.color}; font-weight: bold;")
                    yes_button = QPushButton(get_general_text("yes"))
                    no_button = QPushButton(get_general_text("no"))
                    warning_box.addButton(yes_button, QMessageBox.YesRole)
                    warning_box.addButton(no_button, QMessageBox.NoRole)
                    reply = warning_box.exec_()
                    if reply == QMessageBox.No:
                        return self.change_page(0)
            except:
                warning_text = get_general_text("warning_wrong_type")
            if warning_text:
                warning_box = QMessageBox()
                if get_language() == "de":
                    warning_box.setWindowTitle("Warnung")
                else:
                    warning_box.setWindowTitle("warning")
                warning_box.setText(warning_text)
                warning_box.setStyleSheet(f"color: black; background-color: {self.color}; font-weight: bold;")
                warning_box.exec_()
                return self.change_page(0)
            self.set_basic_permutation_attributes(input_value=input_value)
        self.change_page(page_number)


    def set_basic_permutation_attributes(self, input_value:int) -> None:
        if (self.permutation_group_no is not None and self.permutation_group is not None and
                self.permutation_group_no == input_value and self.permutation_group.permutation_group == input_value):
            return
        self.permutation_group_no = input_value
        self.permutation_group = permutation_group(self.permutation_group_no)


    def update_page(self) -> None:
        """ adding content to layout """
        print("update page Windows:", self.current_page)
        try:
            page_info = next((page_dict for page_dict in self.pages
                              if page_dict.get("index").value == self.current_page), None)
            page_info["function"]()
        except KeyError or TypeError:# todo catch all errors
            self.current_page = 0
            return self.load_main_page()

    def test_page(self) -> None:
        # working equations:
        eqs = [r"E = m \cdot c^ 2", r"\frac{1}{2}", "\\begin{array}{c}{1}\\end{array}", r"\begin{array}{|c|}{2}\end{array}",
               "\\bra{1}"]  # "\\text{a}"]
        for eq in eqs:
            self.add_equation(formula=eq)


    def load_tableau_page(self) -> None:
        # page_info = next((page_dict for page_dict in self.pages if page_dict.get("index") == self.current_page), None)
        self.permutation_group.get_all_standard_tableaus()
        for equation in self.permutation_group.get_young_tableau_equations():
            self.add_equation(formula=equation)

    def load_spin_page(self) -> None:
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
                label = QLabel(get_general_text("spin_2rows"))
                label.setStyleSheet("color: black;")
                self.scroll_layout.addWidget(label)
                self.non_basics.append(label)



    def load_spatial_page(self) -> None:
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
                label = QLabel(get_general_text("spatial_2columns"))
                label.setStyleSheet("color: black;")
                self.scroll_layout.addWidget(label)
                self.non_basics.append(label)

    def load_tableau_page_multiplied(self) -> None:
        label = QLabel(":\n".join(get_title_multiplied_youngtableaus(kind=text_kinds.TXT)))
        label.setStyleSheet("color: black;")
        self.scroll_layout.addWidget(label)
        self.non_basics.append(label)
        for group in self.permutation_group.group_tableaus_by_shortend_symbol(tableaus_to_sort=self.permutation_group.standard_tableaus):
            equation = group[0].get_shortend_symbol()["tex"] + ":"
            self.add_equation(equation)
            for t in group:
                t.set_up_function()
                equation = t.to_tex() + "\quad " + t.function.to_tex()
                self.add_equation(equation)


    def load_main_page(self) -> None:
        print("load_main_page")
        permutation_group_input = QHBoxLayout()
        permutation_group_label = QLabel(get_general_text("input_command"))
        permutation_group_label.setStyleSheet("color: black;")
        permutation_group_input.addWidget(permutation_group_label)
        self.input_box = QLineEdit()
        self.input_box.setStyleSheet("color: black;")
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


    def load_download(self) -> None:
        """ initializes download and goes back to main page """
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet("color: black;")
        self.scroll_layout.addWidget(spacer)
        self.scroll_layout.addWidget(self.progress_bar)
        self.scroll_layout.addWidget(spacer)
        self.non_basics.append(self.progress_bar)
        self.non_basics.append(spacer)

        self.download_thread = DownloadThread(self.permutation_group, self.scroll_layout)
        self.download_thread.update_progress.connect(self.update_progress_bar)
        self.download_thread.start()


    def load_download(self) -> None:
        """ initializes download and goes back to main page """
        spacer = QWidget()#<- for vertical centering
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.progress_bar = QProgressBar()#<- bar to show the progress
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet("color: black;")

        download_layout = QVBoxLayout()
        download_layout.addWidget(spacer)
        download_layout.addWidget(self.progress_bar)
        download_layout.addWidget(spacer)
        # add new layout:
        self.scroll_layout.addLayout(download_layout)
        self.non_basics.append(self.progress_bar)

        # start download thread:
        self.download_thread = DownloadThread(self.permutation_group, self.scroll_layout)
        self.download_thread.update_progress.connect(self.update_progress_bar)
        self.download_thread.start()


    def update_progress_bar(self, value:int, message:str) -> None:
        """
        triggered function (by the download page) that updates the process to show the current status of the download
        :param value: amount of already finished parts of the whole download process (in percent)
        :param message: current process
        :return:
        """
        self.progress_bar.setValue(value)
        self.progress_bar.setFormat(f"{value}%: {message}...")

    def load_overlap_spin(self) -> None:
        title, content, equation = get_title_spin(kind=text_kinds.TXT)
        label = QLabel(title + "\n" + content)
        label.setStyleSheet("color: black;")
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

    def load_overlap_spatial(self) -> None:
        title, content = get_title_spatial(kind=text_kinds.TXT)
        label = QLabel(title+"\n"+content)
        label.setStyleSheet("color: black;")
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


    def load_hamilton_spatial(self) -> None:
        label = QLabel("Hamiltonmatrixelemente für die Raumorbitale"+"\n")
        label.setStyleSheet("color: black;")
        self.scroll_layout.addWidget(label)
        self.non_basics.append(label)

        self.permutation_group.calculate_all_hamilton_integrals()
        for info in self.permutation_group.hamilton_integrals:
            if len(info["hamilton_integral_sum"]) > 0:
                equation_tex = r"\bra{"+ info["bra_tableau"] + r"}\hat{H}\ket{"+ info["ket_tableau"] + r"}"
                if info["kind"] == spin_vs_spatial_kind.SPATIAL.value:
                    equation_tex+=r"_{\Phi}"
                equation_tex += " = "
                for addend in info["hamilton_integral_sum"]:
                    equation_tex += addend.to_tex()
                self.add_equation(equation_tex)



    def load_hamilton_spin(self) -> None:
        label = QLabel(get_general_text("h_info_spin")+"\n\n")
        label.setStyleSheet("color: red; font-weight: bold;")
        self.scroll_layout.addWidget(label)
        self.non_basics.append(label)

        self.load_overlap_spin()
















if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindows()
    window.show()
    sys.exit(app.exec_())
