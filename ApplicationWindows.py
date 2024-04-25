
import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QLabel,QLineEdit, QMessageBox, QSizePolicy


from MainApplication import MainApplication



class ApplicationWindows(MainApplication):

    def __init__(self):
        super().__init__()


    def update_page(self):
        print("update page Windows")
        if self.current_page == 0:
            self.load_mainpage()
        else:
            super().update_page()

    def load_mainpage(self):
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
        self.scroll_layout.setStretch(self.scroll_layout.indexOf(spacer), 1)

        self.non_basics.append(permutation_group_label)
        self.non_basics.append(permutation_group_input)
        self.non_basics.append(self.input_box)


    def open_page(self, page_number:int):
        """ checking the input and (if the input is okay) loading another page """
        # getting and checking the input information:
        if page_number == 0:
            return self.change_page(page_number)
        input_value = self.input_box.text()
        if not input_value:
            QMessageBox.warning(self, "Warnung", "Bitte geben Sie eine Permutationsgruppe ein.")
            return  self.change_page(0)
        try:
            input_value = int(input_value)
            if input_value <= 0:
                QMessageBox.warning(self, "Warnung", "Bitte geben Sie eine Permutationsgruppe als positive Zahl.")
                return  self.change_page(0)
        except:
            QMessageBox.warning(self, "Warnung", "Bitte geben Sie die Nummer für eine Permutationsgruppe ein.")
            return  self.change_page(0)
        self.change_page(page_number)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindows()
    window.show()
    sys.exit(app.exec_())
