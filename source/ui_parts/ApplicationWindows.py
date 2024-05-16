
import sys
from typing import Union

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QSizePolicy, \
    QProgressBar, QPushButton, QVBoxLayout, QSpacerItem

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
                    warning_box.setStyleSheet(f"color: {self.color.value['text']}; background-color: {self.color.value['background']}; font-weight: bold;")
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
                warning_box.setWindowTitle(get_general_text("warning"))
                warning_box.setTextFormat(Qt.RichText)
                warning_box.setText(f"<b>{warning_text}</b>")
                warning_box.setStyleSheet(f"color: {self.color.value['text']}; background-color: {self.color.value['background']}; font-weight: bold;")
                warning_box.exec_()
                return self.change_page(0)
            self.set_basic_permutation_attributes(input_value=input_value)
        self.change_page(page_number)


    def set_basic_permutation_attributes(self, input_value:int) -> None:
        """
        using the input to set the group object on which calculations may occur
        :param input_value: number of permutation group, as given in the input box
        """
        if (self.permutation_group_no is not None and self.permutation_group is not None and
                self.permutation_group_no == input_value and self.permutation_group.permutation_group == input_value):
            return
        self.permutation_group_no = input_value
        del self.permutation_group # remove, to allow a new instance
        self.permutation_group = permutation_group(self.permutation_group_no)


    def update_page(self) -> None:
        """ adding content (in between general buttons at the top and information bar at the bottom) to layout """
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
        #todo:
        tst = (r"1 \cdot 2 = E \cdot c^2")
        self.add_equation(tst)

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
                label.setStyleSheet(f"color: {self.color.value['text']};")
                self.scroll_layout.addWidget(label)



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
                label.setStyleSheet(f"color: {self.color.value['text']};")
                self.scroll_layout.addWidget(label)

    def load_tableau_page_multiplied(self) -> None:
        label = QLabel(":\n".join(get_title_multiplied_youngtableaus(kind=text_kinds.TXT)))
        label.setStyleSheet(f"color: {self.color.value['text']};")
        self.scroll_layout.addWidget(label)
        for group in self.permutation_group.group_tableaus_by_shortend_symbol(tableaus_to_sort=self.permutation_group.standard_tableaus):
            equation = group[0].get_shortend_symbol()["tex"] + ":"
            self.add_equation(equation)
            for t in group:
                t.set_up_function()
                equation = t.to_tex() + "\quad " + t.function.to_tex()
                self.add_equation(equation)


    def load_main_page(self) -> None:
        permutation_group_input = QVBoxLayout()
        permutation_group_input.setAlignment(Qt.AlignCenter)
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        permutation_group_input.addItem(spacer_top)

        hbox = QHBoxLayout()# to put label and input in 1 line
        hbox.setAlignment(Qt.AlignCenter)

        permutation_group_label = QLabel(get_general_text("input_command"))
        permutation_group_label.setStyleSheet(f"color: {self.color.value['text']}; font-size: 15pt;")
        hbox.addWidget(permutation_group_label)

        self.input_box = QLineEdit()
        self.input_box.setStyleSheet(f"color: {self.color.value['text']};")
        self.input_box.setToolTip(get_general_text("input_line_command"))
        self.input_box.enterEvent = lambda event, input=input: self.change_status_message(self.input_box.toolTip())
        self.input_box.leaveEvent = lambda event: self.change_status_message()
        hbox.addWidget(self.input_box)

        permutation_group_input.addLayout(hbox)
        # permutation_group_input.addStretch(1)# input not completely at the bottom
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        permutation_group_input.addItem(spacer_top)
        self.scroll_layout.addLayout(permutation_group_input)


    def load_download(self) -> None:
        """ initializes download and goes back to main page """
        label = QLabel(get_general_text("download_start_info1")+str(self.permutation_group_no)+get_general_text("download_start_info2")+"\n")
        label.setStyleSheet(f"color: bla{self.color.value['text']}ck;")

        self.progress_bar = QProgressBar()#<- bar to show the progress
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet(f"color: {self.color.value['text']};")

        download_layout = QVBoxLayout()
        download_layout.setAlignment(Qt.AlignCenter)
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        download_layout.addItem(spacer_top)


        download_layout.addWidget(label)
        download_layout.addWidget(self.progress_bar)
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        download_layout.addItem(spacer_top)
        # add new layout:
        self.scroll_layout.addLayout(download_layout)

        # start download thread:
        self.download_thread = DownloadThread(self.permutation_group, self.scroll_layout, background_color=self.color.value['background'])
        self.download_thread.enable_all_buttons(activated=False)
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
        label.setStyleSheet(f"color: {self.color.value['text']};")
        self.scroll_layout.addWidget(label)
        self.add_equation(equation)
        for i in self.permutation_group.overlap:
            if (i['kind'] == spin_vs_spatial_kind.SPIN and len(i['result'].parts) == 1 and
                    i['result'].parts[0].factor != 0 and i['result'].parts[0].factor != 1):
                equation_tex = get_dirac_notation(str(i['bra_tableau']), str(i['ket_tableau']), kind=text_kinds.TEX)
                equation_tex += r"_{\sigma }"
                equation_tex += "=" + get_dirac_notation(str(i['bra']), str(i['ket']), kind=text_kinds.TEX)
                equation_tex += r"_{\Phi}"
                equation_tex += f" = {i['result'].to_tex()}"
                self.add_equation(equation_tex)
        if len(self.permutation_group.overlap) == 0:
            label = QLabel(fr"<p><b>!</b> <textit>{get_general_text('too_small_for_overlap')}<\textit></p>")#todo
            label.setTextFormat(Qt.RichText)
            self.scroll_layout.addWidget(label)


    def load_overlap_spatial(self) -> None:
        title, content = get_title_spatial(kind=text_kinds.TXT)
        label = QLabel(title+"\n"+content)
        label.setStyleSheet(f"color: {self.color.value['text']};")
        self.scroll_layout.addWidget(label)
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
        if len(self.permutation_group.overlap) == 0:
            label = QLabel(fr"<p><b>!</b> <textit>{get_general_text('too_small_for_overlap')}<\textit></p>")#todo
            label.setTextFormat(Qt.RichText)
            self.scroll_layout.addWidget(label)


    def load_hamilton_spatial(self) -> None:
        label = QLabel("Hamiltonmatrixelemente für die Raumorbitale"+"\n")
        label.setStyleSheet(f"color: {self.color.value['text']};")
        self.scroll_layout.addWidget(label)
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
        if len(self.permutation_group.hamilton_integrals) == 0:
            label = QLabel(fr"<p><b>!</b> <textit>{get_general_text('too_small_for_overlap')}<\textit></p>")#todo
            label.setTextFormat(Qt.RichText)
            self.scroll_layout.addWidget(label)



    def load_hamilton_spin(self) -> None:
        label = QLabel(get_general_text("h_info_spin")+"\n\n")
        label.setStyleSheet("color: darkred; font-weight: bold;")
        self.scroll_layout.addWidget(label)

        self.load_overlap_spin()
















if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindows()
    window.show()
    sys.exit(app.exec_())
