from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
matplotlib.rcParams['text.usetex'] = True

from source.permutation_group import permutation_group


class PageYoungTableaus(QWidget):
    def __init__(self, permutation_group:int, parent=None):
        super().__init__(parent)#main page
        self.layout = parent.layout
        self.permutation_group = permutation_group
        self.label = QLabel(f"Die möglichen (Standard-)Young-Tableaus zur Gruppe {self.permutation_group} lauten:")
        self.layout.addWidget(self.label)

        self.get_content()
        self.add_buttons(parent)


    def add_buttons(self, parent):
        self.back_button = QPushButton("zurück")
        self.back_button.clicked.connect(parent.back_to_start)
        self.layout.addWidget(self.back_button)


    def get_content(self):
        """ get all standard tableaus for the given group """
        p = permutation_group(self.permutation_group)
        p.get_all_standard_tableaus()
        # self.parent.add_equation("e \cdot b")
        for t in p.standard_tableaus:
            self.add_equation(eq=t.to_tex())

    def add_equation(self, eq: str):
        figure = plt.figure()
        ax = figure.add_subplot(111)
        ax.text(0.05, 0.5, f"${eq}$",
                horizontalalignment='left', verticalalignment='center', fontsize=20)
        ax.axis('off')
        figure.patch.set_facecolor('none')

        bbox = ax.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
        width = int(bbox.width * figure.dpi)
        height = int(bbox.height * figure.dpi/3)
        canvas = FigureCanvas(figure)
        canvas.setFixedSize(width, height)

        self.layout.addWidget(canvas, alignment=Qt.AlignLeft)
        plt.close(figure)


