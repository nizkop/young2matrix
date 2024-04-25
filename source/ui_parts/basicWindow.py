from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
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

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setAlignment(Qt.AlignCenter)#TODO: this doesnt change anything!?

    # def back_to_start(self):
    #     self.clearLayout()
    #     pass # to adapt in each subclass of basicWindow

    def add_equation(self, eq: str):
        """
        :param eq: latex-formatted equation, e.g.r"\frac{1}{2} \cdot \pi"
        """
        # equation_widget = QWidget()
        # equation_layout = QVBoxLayout(equation_widget)

        figure = plt.figure()
        ax = figure.add_subplot(111)
        ax.text(0.05, 0.5, rf"${eq}$", horizontalalignment='left', verticalalignment='center', fontsize=20)
        ax.axis('off')
        figure.patch.set_facecolor('none')
        plt.tight_layout(pad=0.2)

        bbox = ax.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
        width = int(bbox.width * figure.dpi)
        height = int(bbox.height * figure.dpi/3) # suited for tableau [(1,2,3)], for other equations to high
        canvas = FigureCanvas(figure)
        canvas.setFixedSize(width, height)

        self.layout.addWidget(canvas, alignment=Qt.AlignLeft)
        # equation_widget.setLayout(equation_layout)
        #
        # self.layout.addWidget(equation_widget)
        plt.close(figure)

    def add_buttons(self):
        self.back_button = QPushButton("zurück zum Start")
        self.back_button.clicked.connect(self.main.back_to_start)
        self.back_button.setMaximumWidth(200)
        self.buttons_layout.addWidget(self.back_button)
        self.layout.addLayout(self.buttons_layout)
        self.layout.setAlignment(Qt.AlignHCenter)


    def show_previous_page(self):
        if self.parent:
            self.parent.back_to_start()
        self.main.back_to_start()


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
