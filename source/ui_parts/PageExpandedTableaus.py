from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLabel
import matplotlib

from source.texts.get_titles_for_permutation_parts import get_title_permutation_to_tableaus

matplotlib.rcParams['text.usetex'] = True

from source.ui_parts.basicWindow import basicWindow
from source.permutation_group import permutation_group



class PageExpandedTableaus(basicWindow):
    def __init__(self, permutation_group:int, parent#: PageYoungTableau
                 , main#:StartWindow
                 ):
        super().__init__(permutation_group=permutation_group, main=main, parent=parent)
        self.back_to_start()

    def back_to_start(self):
        self.label = QLabel(get_title_permutation_to_tableaus(self.permutation_group))
        self.layout.addWidget(self.label)

        self.get_content()
        self.add_buttons()

    def add_buttons(self):
        super().add_buttons()

        self.back_button_tableaus = QPushButton("zurück")
        self.back_button_tableaus.clicked.connect(self.parent.back_to_start)
        self.back_button_tableaus.setMaximumWidth(200)
        self.buttons_layout.addWidget(self.back_button_tableaus)
        self.layout.addLayout(self.buttons_layout)
        self.layout.setAlignment(Qt.AlignHCenter)

    def get_content(self):
        """ get all standard tableaus for the given group """
        p = permutation_group(self.permutation_group)
        p.get_all_standard_tableaus()
        for group in p.group_tableaus_by_shortend_symbol(tableaus_to_sort=p.standard_tableaus):
            equation = group[0].get_shortend_symbol()["tex"] + ":"
            self.add_equation(eq=equation)
            for t in group:
                t.set_up_function()
                equation = t.to_tex() + "\quad " + t.function.to_tex()
                self.add_equation(eq=equation)