from PyQt5.QtCore import QThread, pyqtSignal
import time

from source.texts.general_texts import get_general_text
from source.ui_parts.settings.idea_config import get_language


class DownloadThread(QThread):
    """ needed to show download progress during the process """
    update_progress = pyqtSignal(int,str)  # signal
    def __init__(self, permutation_group):
        super().__init__()
        self.permutation_group = permutation_group

    def run(self) -> None:
        """
        splitting the download into sub-processes and assigning each a percent value (to describe the progress)
        """
        try:
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
            self.update_progress.emit(-1,get_general_text("failed_download"))
        finally:
            self.update_progress.emit(100,get_general_text("successful_download"))


