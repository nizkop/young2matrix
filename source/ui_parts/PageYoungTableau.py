from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib

from source.ui_parts.PageExpandedTableaus import PageExpandedTableaus
from source.ui_parts.basicWindow import basicWindow

matplotlib.rcParams['text.usetex'] = True

from source.permutation_group import permutation_group


class PageYoungTableaus(basicWindow):
    def __init__(self, permutation_group:int, parent#:StartWindow
                ):
        super().__init__(permutation_group=permutation_group, main=parent)#main page

        self.back_to_start()

    def add_buttons(self):
        super().add_buttons()

        self.further_button = QPushButton("Tableaus ausmultiplizieren")
        self.further_button.clicked.connect(self.on_further_button_clicked)
        self.layout.addWidget(self.further_button)

    def back_to_start(self):
        self.clearLayout()
        self.label = QLabel(f"Die möglichen (Standard-)Young-Tableaus zur Gruppe {self.permutation_group} lauten:")
        self.layout.addWidget(self.label)

        self.get_content()
        self.add_buttons()

    def on_further_button_clicked(self):
        self.clearLayout()
        PageExpandedTableaus(permutation_group=self.permutation_group, parent=self, main=self.main)


    def get_content(self):
        """ get all standard tableaus for the given group """
        p = permutation_group(self.permutation_group)
        p.get_all_standard_tableaus()
        for group in p.group_tableaus_by_shortend_symbol(tableaus_to_sort=p.get_non_adjoint_tableaus()):
            equation = r"\quad , \quad ".join([t.to_tex() for t in group])
            self.add_equation(eq=equation)

    # def add_equation(self, eq: str):
    #     figure = plt.figure()
    #     ax = figure.add_subplot(111)
    #     ax.text(0.05, 0.5, f"${eq}$",
    #             horizontalalignment='left', verticalalignment='center', fontsize=20)
    #     ax.axis('off')
    #     figure.patch.set_facecolor('none')
    #
    #     bbox = ax.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
    #     width = int(bbox.width * figure.dpi)
    #     height = int(bbox.height * figure.dpi/3)
    #     canvas = FigureCanvas(figure)
    #     canvas.setFixedSize(width, height)
    #
    #     self.layout.addWidget(canvas, alignment=Qt.AlignLeft)
    #     plt.close(figure)


