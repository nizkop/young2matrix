import time
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QLabel

from source.PermutationGroup import PermutationGroup
from source.settings.settings_config import get_color, get_language
from source.texts.general_texts import get_general_text
from source.ui_parts.get_basic_formatting_for_layout_part import format_layout_part
from source.settings.LanguageChoices import LanguageChoices


class DownloadThread(QThread):
    """ needed to show download progress during the process """
    update_progress = pyqtSignal(int, str)  # signal handling percentage of process and status message

    def __init__(self, permutation_group:PermutationGroup, status_label:QLabel, background_color:str, text_color:str, buttons):
        super().__init__()
        self.permutation_group = permutation_group
        self.buttons = buttons
        self.background_color = background_color
        self.text_color = text_color
        self.status_label = status_label


    def enable_all_buttons(self, activated:bool) -> None:
        """
        de/activating all buttons in the current layout (while a process is running)
        showing the disabling by color change (this function can do everything for that except the icon color of the settings button)
        :param activated: boolean indicating whether buttons are activated or deactivated
        """
        for button in self.buttons:
            try:
                button.setEnabled(activated)
                if activated:
                    format_layout_part(button) # reset
                else:
                    color = get_color()
                    format_layout_part(button,
                        f"background-color: {color['deactivated-button']}; color:{color['disabled-text']};")
            except Exception as e:
                print(e, flush=True)
                pass # button already deleted


    def run(self) -> None:
        """
        splitting the download into sub-processes and assigning each a percent value (to describe the progress)
        """
        self.enable_all_buttons(activated=False)
        time.sleep(1)

        try:
            self.update_progress.emit(10,"finding all tableaus" if get_language() == LanguageChoices.en.name
                                      else "Finden aller Tableaus")
            self.permutation_group.get_all_standard_tableaus()  # at least needed for chapter 4
            time.sleep(1)

            self.update_progress.emit(30,"calculating all tableaus" if get_language() == LanguageChoices.en.name
                                    else "Berechnung aller Tableaus")
            self.permutation_group.get_chapter_youngtableaus()
            time.sleep(1)

            self.update_progress.emit(40,"multiplying out the tableaus" if get_language() == LanguageChoices.en.name
                                    else "Ausmultiplizieren der Tableaus")
            self.permutation_group.get_chapter_multiplied()
            time.sleep(1)

            self.update_progress.emit(50,"setting up spin-based tableaus" if get_language() == LanguageChoices.en.name
                                    else "Aufsetzen der Spinfunktionstableaus")
            self.permutation_group.get_chapter_spinfunctions()
            self.permutation_group.get_chapter_spinfunctions()
            time.sleep(1)

            self.update_progress.emit(70,"calculating overlap integrals" if get_language() == LanguageChoices.en.name
                                    else "Berechnung der Überlappintegrale")
            self.permutation_group.get_chapter_overlapintegrals()
            time.sleep(1)

            self.update_progress.emit(90,"calculating hamilton integrals" if get_language() == LanguageChoices.en.name
                                      else "Berechnung der Hamiltonintegrale")
            self.permutation_group.get_chapter_hamiltonintegrals()
            time.sleep(1)

            self.update_progress.emit(95,"saving pdf" if get_language() == LanguageChoices.en.name
                                        else "PDF abspeichern")
            self.permutation_group.overview.save()
            time.sleep(1)
            # todo: matrix?
        except Exception:
            self.update_progress.emit(-1,get_general_text("failed_download"))
        else:
            self.update_progress.emit(100,get_general_text("successful_download"))
        finally:
            self.enable_all_buttons(True)


