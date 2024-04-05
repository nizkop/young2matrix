from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib

from source.ui_parts.basicWindow import basicWindow

matplotlib.rcParams['text.usetex'] = True

from source.permutation_group import permutation_group



class PageExpandedTableaus(basicWindow):
    def __init__(self, permutation_group:int, parent#: PageYoungTableau
                 , main#:StartWindow
                 ):
        super().__init__(permutation_group=permutation_group, main=main, parent=parent)
        self.back_to_start()

    def back_to_start(self):
        self.label = QLabel(f"Die möglichen (Standard-)Young-Tableaus zur Gruppe {self.permutation_group} lauten:")
        self.layout.addWidget(self.label)

        self.get_content()
        self.add_buttons()


    def add_buttons(self):
        super().add_buttons()

        self.back_button = QPushButton("zurück")
        self.back_button.clicked.connect(self.parent.back_to_start)
        self.layout.addWidget(self.back_button)


    def get_content(self):
        """ get all standard tableaus for the given group """
        p = permutation_group(self.permutation_group)
        p.get_all_standard_tableaus()
        for group in p.group_tableaus_by_shortend_symbol(tableaus_to_sort=p.get_non_adjoint_tableaus()):
            for t in group:
                t.set_up_function()
                equation = t.to_tex() + "\quad " + t.function.to_tex()
                self.add_equation(eq=equation)