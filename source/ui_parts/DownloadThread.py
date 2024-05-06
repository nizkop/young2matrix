import time
from typing import List

from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLayoutItem, QWidgetItem

from source.permutation_group import permutation_group
from source.texts.general_texts import get_general_text
from source.ui_parts.settings.idea_config import get_language


class DownloadThread(QThread):
    """ needed to show download progress during the process """
    update_progress = pyqtSignal(int,str)  # signal
    def __init__(self, permutation_group:permutation_group, layout: QVBoxLayout):
        super().__init__()
        self.permutation_group = permutation_group
        self.scroll_layout = layout

    def get_buttons_from_layout(self, layout=None) -> List[QPushButton]:
        """
        searching for buttons in the given/current layout
        :param layout: layout / sublayout (needed to search recursively through all sub layouts)
        :return: list of all buttons
        """
        if layout == None:
            layout = self.scroll_layout
        buttons = []
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if isinstance(item, QWidgetItem):
                widget = item.widget()
                if isinstance(widget, QPushButton):
                    buttons.append(widget)
            elif isinstance(item, QLayoutItem):
                inner_layout = item.layout()
                if inner_layout:
                    buttons.extend(self.get_buttons_from_layout(inner_layout))
        return buttons

    def enable_all_buttons(self, activated:bool) -> None:
        """
        de/activating all buttons in the current layout (while a process is running)
        :param activated: boolean indicating whether buttons are activated or deactivated
        """
        for button in self.get_buttons_from_layout():
            button.setEnabled(activated)

    def run(self) -> None:
        """
        splitting the download into sub-processes and assigning each a percent value (to describe the progress)
        """
        try:
            self.enable_all_buttons(activated=False)
            self.update_progress.emit(10, "finding all tableaus")
            self.permutation_group.get_all_standard_tableaus()  # at least needed for chapter 4
            time.sleep(1)

            self.update_progress.emit(30,"calculating all tableaus" if get_language()== "en" else "Berechnung aller Tableaus")
            self.permutation_group.get_chapter_youngtableaus()
            time.sleep(1)

            self.update_progress.emit(40,"multiplying out the tableaus" if get_language()=="en" else "Ausmultiplizieren der Tableaus")
            self.permutation_group.get_chapter_multiplied()
            time.sleep(1)

            self.update_progress.emit(50,"setting up spin-based tableaus" if get_language()=="en" else "Aufsetzen der Spinfunktionstableaus")
            self.permutation_group.get_chapter_spinfunctions()
            time.sleep(1)

            self.update_progress.emit(70,"calculating overlap integrals" if get_language()=="en" else "Berechnung der Überlappintegrale")
            self.permutation_group.get_chapter_overlapintegrals()
            time.sleep(1)

            self.update_progress.emit(90,"calculating hamilton integrals" if get_language()=="en" else "Berechnung der Hamiltonintegrale")
            self.permutation_group.get_chapter_hamiltonintegrals()
            time.sleep(1)

            self.update_progress.emit(95,"saving pdf" if get_language()=="en" else "PDF abspeichern")
            self.permutation_group.overview.save(title=self.permutation_group.title_pdf)
            time.sleep(1)
            # todo: matrix?
        except:
            self.enable_all_buttons(True)
            self.update_progress.emit(-1, get_general_text("failed_download"))
        finally:
            self.enable_all_buttons(True)
            self.update_progress.emit(100,get_general_text("successful_download"))


