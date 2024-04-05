from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib


matplotlib.rcParams['text.usetex'] = True


class basicWindow(QWidget):
    def __init__(self, main, permutation_group:int, parent=None):
        super().__init__(main)
        self.main = main # main page
        self.layout = main.layout
        if parent is not None:
            self.parent = parent
            self.layout = self.parent.layout
        self.permutation_group = permutation_group

    def back_to_start(self):
        self.clearLayout()
        pass # to adapt in each subclass of basicWindow

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

    def add_buttons(self):
        self.back_button = QPushButton("zurück zum Start")
        self.back_button.clicked.connect(self.main.back_to_start)
        self.layout.addWidget(self.back_button)

    def show_previous_page(self):
        if self.parent:
            self.parent.back_to_start()
        self.mein.back_to_start()


    def clearLayout(self, layout=None) -> None:
        """ Clearing the current layout and its sublayouts
         :param layout: in function call None, but in recursion a sublayout can be referenced here
         """
        if layout is None:
            layout = self.layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
            else:
                sublayout = item.layout()
                if sublayout:
                    self.clearLayout(layout=sublayout)
