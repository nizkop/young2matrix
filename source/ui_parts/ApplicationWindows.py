import math
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
from source.texts.get_info_spin_possibilities import get_info_spin_possibilities
from source.texts.get_title_spatial import get_title_spatial
from source.texts.get_title_spin import get_title_spin
from source.texts.get_title_youngtableaus import get_title_multiplied_youngtableaus
from source.texts.get_titles_for_permutation_parts import get_title_permutation_to_tableaus
from source.ui_parts.MainApplication import MainApplication
from source.ui_parts.DownloadThread import DownloadThread
from source.ui_parts.get_basic_formatting_for_layout_part import format_layout_part
from source.ui_parts.settings.settings_config import get_color, load_config



class ApplicationWindows(MainApplication):
    """
    class needed to fill ui pages of main application with actual content;
    the chemical content (permutation group) is brought in here
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
                    format_layout_part(warning_box)#f"color: {self.color.value['text']}; background-color: {self.color.value['background']}; font-weight: bold;")
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
                format_layout_part(warning_box)#f"color: {self.color.value['text']}; background-color: {self.color.value['background']}; font-weight: bold;")
                warning_box.exec_()
                return self.change_page(0)
            self.set_basic_permutation_attributes(input_value=input_value)
        self.change_page(page_number)
        self.scroll_area.verticalScrollBar().setValue(0)#scroll to the top (for the new page)
        self.scroll_area.horizontalScrollBar().setValue(0)#in case of long equations

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


    ###   single pages   ############################################################################################
    def test_page(self) -> None:
        # working equations:
        eqs = [r"E = m \cdot c^ 2", r"\frac{1}{2}", "\\begin{array}{c}{1}\\end{array}", r"\begin{array}{|c|}{2}\end{array}",
               "\\bra{1}"]  # "\\text{a}"]
        for eq in eqs:
            self.add_equation(formula=eq)

    def update_progress_bar(self, value:int, message:str) -> None:
        """
        triggered function (by the download page) that updates the process to show the current status of the download
        :param value: amount of already finished parts of the whole download process (in percent)
        :param message: current process
        :return:
        """
        self.progress_bar.setValue(value)
        self.progress_bar.setFormat(f"{value}%: {message}...")

    def load_main_page(self) -> None:
        permutation_group_input = QVBoxLayout()
        permutation_group_input.setAlignment(Qt.AlignCenter)
        spacer_top = QSpacerItem(0, self.spacer_height, QSizePolicy.Minimum, QSizePolicy.Expanding)
        permutation_group_input.addItem(spacer_top)

        hbox = QHBoxLayout()# to put label and input in 1 line
        hbox.setAlignment(Qt.AlignCenter)
        hbox.addSpacing(load_config()['button-size'])

        permutation_group_label = QLabel(get_general_text("input_command"))
        permutation_group_label.setWordWrap(True)
        permutation_group_label.setMaximumWidth(self.width())
        format_layout_part(permutation_group_label)#f"color: {self.color.value['text']}; font-size: {self.font_size}pt;")
        hbox.addWidget(permutation_group_label)
        hbox.addSpacing(load_config()['button-size'])# distance between label and input box

        self.input_box = QLineEdit()
        format_layout_part(self.input_box)#f"color: {self.color.value['text']};")
        self.input_box.setToolTip(f"<span style='font-size:{load_config()['font-size']}pt;'>{get_general_text('input_line_command')}</span>")
        self.input_box.enterEvent = lambda event, input=input: (
                                            self.change_status_message(get_general_text('input_line_command')))
        self.input_box.leaveEvent = lambda event: self.change_status_message()
        self.input_box.setMaximumWidth(max(load_config()['button-size'], math.ceil(self.width()/4)))
        hbox.addWidget(self.input_box)
        self.input_box.setAlignment(Qt.AlignLeft)

        hbox.addStretch()#avoid input line totally on the right
        permutation_group_input.addLayout(hbox)
        self.scroll_layout.addLayout(permutation_group_input)

    def load_tableau_page(self) -> None:
        self.set_ui_label(header=get_general_text('tableau_header'),
                     content=get_title_permutation_to_tableaus(self.permutation_group.permutation_group))
        # page_info = next((page_dict for page_dict in self.pages if page_dict.get("index") == self.current_page), None)
        self.permutation_group.get_all_standard_tableaus()
        for equation in self.permutation_group.get_young_tableau_equations():
            self.add_equation(formula=equation)

    def load_tableau_page_multiplied(self) -> None:
        header, content = get_title_multiplied_youngtableaus(kind=text_kinds.TXT)
        self.set_ui_label(header=header, content=content)
        for group in self.permutation_group.group_tableaus_by_shortend_symbol(tableaus_to_sort=self.permutation_group.standard_tableaus):
            equation = group[0].get_shortend_symbol()["tex"] + ":"
            self.add_equation(equation)
            for t in group:
                t.set_up_function()
                equation = t.to_tex() + "\quad " + t.function.to_tex()
                self.add_equation(equation)

    def load_spin_page(self) -> None:
        self.set_ui_label(header=get_general_text('spin_header'),
                 content = get_info_spin_possibilities(self.permutation_group.permutation_group, kind=text_kinds.TXT))
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
                self.set_ui_label(content = get_general_text("spin_2rows"))

    def load_spatial_page(self) -> None:
        self.set_ui_label(header=get_general_text("spatial_header"), content=get_title_multiplied_youngtableaus(text_kinds.TXT)[1])
        self.permutation_group.get_all_standard_tableaus()
        groups = self.permutation_group.group_tableaus_by_shortend_symbol(
                tableaus_to_sort=self.permutation_group.standard_tableaus)
        for group in groups:
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
                self.set_ui_label(content = get_general_text("spatial_2columns"))

    def load_overlap_spin(self) -> None:
        title, content, equation = get_title_spin(kind=text_kinds.TXT)
        self.set_ui_label(header=get_general_text("overlap_header")+title, spacing=False,
                          content=content.replace(r"\n","<br>"))
        label = QLabel(equation)
        label.setWordWrap(True)
        label.setMaximumWidth(self.width())
        self.scroll_layout.addWidget(label)
        # actual equations for this case:
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
            label = QLabel(fr"<p><b>!</b> <i>{get_general_text('too_small_for_overlap')}<\i></p>")
            label.setWordWrap(True)
            label.setMaximumWidth(self.width())
            label.setTextFormat(Qt.RichText)
            self.scroll_layout.addWidget(label)

    def load_overlap_spatial(self) -> None:
        title, content = get_title_spatial(kind=text_kinds.TXT)
        self.set_ui_label(header=get_general_text("overlap_header")+title, content=content)
        self.permutation_group.calculate_all_overlap_integrals()
        empty = True
        for i in self.permutation_group.overlap:
            if i['kind'] == spin_vs_spatial_kind.SPATIAL and len(i['result'].parts) == 1 and i['result'].parts[
                0].factor != 0 and i['result'].parts[0].factor != 1:
                empty = False
                equation_tex = get_dirac_notation(str(i['bra_tableau']), str(i['ket_tableau']), kind=text_kinds.TEX)
                if i['kind'] == spin_vs_spatial_kind.SPIN:
                    equation_tex += r"_{\sigma }"
                    equation_tex += "=" + get_dirac_notation(str(i['bra']), str(i['ket']), kind=text_kinds.TEX)
                equation_tex += r"_{\Phi}"
                equation_tex += f" = {i['result'].to_tex()}"
                self.add_equation(equation_tex)
        if len(self.permutation_group.overlap) == 0 or empty:
            label = QLabel(fr"<p><b>!</b> <i>{get_general_text('too_small_for_overlap')}<\i></p>")
            label.setWordWrap(True)
            label.setMaximumWidth(self.width())
            label.setTextFormat(Qt.RichText)
            self.scroll_layout.addWidget(label)

    def load_hamilton_spatial(self) -> None:
        self.set_ui_label(header=get_general_text("header_hamilton_spatial"))
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
            label = QLabel(fr"<p><b>!</b> <i>{get_general_text('too_small_for_overlap')}<\i></p>")
            label.setWordWrap(True)
            label.setMaximumWidth(self.width())
            label.setTextFormat(Qt.RichText)
            self.scroll_layout.addWidget(label)

    def load_hamilton_spin(self) -> None:
        self.set_ui_label(header=get_general_text("header_hamilton_spin"))
        label = QLabel(get_general_text("h_info_spin")+"\n\n")
        label.setWordWrap(True)
        label.setMaximumWidth(self.width())
        format_layout_part(label, added_style ="color: darkred; font-weight: bold;")
        self.scroll_layout.addWidget(label)

        self.load_overlap_spin()

    def load_download(self) -> None:
        """ initializes download and goes back to main page """
        print("load download", flush=True)
        label = QLabel(get_general_text("download_start_info1")+str(self.permutation_group_no)+get_general_text("download_start_info2")+"\n")
        format_layout_part(label)

        self.progress_bar = QProgressBar()#<- bar to show the progress
        # self.progress_bar.setStyleSheet(f"background-color: {get_color()['status-background']};")
        self.progress_bar.setRange(0, 100)
        format_layout_part(self.progress_bar)
        # print("progress:", get_color()['status_background'], flush=True)


        download_layout = QVBoxLayout()
        download_layout.setAlignment(Qt.AlignCenter)
        spacer_top = QSpacerItem(0, self.spacer_height, QSizePolicy.Minimum, QSizePolicy.Expanding)
        download_layout.addItem(spacer_top)


        download_layout.addWidget(label)
        download_layout.addWidget(self.progress_bar)
        spacer_top = QSpacerItem(0, self.spacer_height, QSizePolicy.Minimum, QSizePolicy.Expanding)
        download_layout.addItem(spacer_top)
        # add new layout:
        self.scroll_layout.addLayout(download_layout)

        # start download thread:
        self.download_thread = DownloadThread(self.permutation_group, self.scroll_layout,
                                              background_color=get_color()['background'], text_color=get_color()["text"])
        self.download_thread.enable_all_buttons(activated=False)
        self.download_thread.update_progress.connect(self.update_progress_bar)
        self.download_thread.start()
















if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindows()
    window.show()
    sys.exit(app.exec_())
