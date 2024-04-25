import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, \
    QScrollArea
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.non_basics = []
        self.setWindowTitle("young2matrix")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        self.setStyleSheet("background-color: lightgreen;")

        self.current_page = 0
        self.pages = [
            ("Startseite",[]),
            ("Seite 1", [r"\sum_{i=1}^{n} i^2", r"E = m \cdot c ^2"]),
            ("Seite 2", [r"e^{i\pi} + 1 = 0"])
        ]

        self.label = QLabel()
        self.label.setStyleSheet("background-color: transparent;")
        self.scroll_layout.addWidget(self.label)# inserts a bit of vertical space (thereby not in create_widget)

        self.create_widgets()


    def create_widgets(self):
        print("create widgets", flush=True)


        self.update_page() #content above buttons

        button_layout = QHBoxLayout()  # horizontal layout (for buttons)

        for i, (text, _) in enumerate(self.pages):
            button = QPushButton(text)
            button.setStyleSheet("background-color: lightgreen;")
            button.clicked.connect(lambda _, i=i: self.open_page(i))
            button_layout.addWidget(button)
            self.non_basics.append(button)

        self.scroll_layout.addLayout(button_layout)
        self.non_basics.append(button_layout)

    def open_page(self, page_number:int):
        """
        to be implemented in sub-class
        :param i:
        :return:
        """
        return self.change_page(page_number)

    def update_page(self):
        print("update_page", flush=True)
        _, formulas = self.pages[self.current_page]

        for formula in formulas:
            self.add_equation(formula)

    def add_equation(self, formula: str):
        """
        :param formula: latex-formatted equation, e.g. r"\frac{1}{2} \cdot \pi"
        """
        print("add_equation", flush=True)

        figure = Figure()
        ax = figure.add_subplot(111)
        ax.text(0.05, 0.5, rf"${formula}$", horizontalalignment='left', verticalalignment='center', fontsize=20)
        ax.axis('off')
        figure.patch.set_facecolor('none')

        bbox = ax.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
        width = int(bbox.width * figure.dpi)
        height = int(bbox.height * figure.dpi/3)
        canvas = FigureCanvas(figure)
        canvas.setFixedSize(width, height)

        self.scroll_layout.addWidget(canvas, alignment=Qt.AlignLeft)
        self.non_basics.append(canvas)
        figure.tight_layout(pad=0.2)
        figure.canvas.draw()

    def change_page(self, index):
        print("change page",flush=True)
        self.current_page = index
        self.clearLayout()
        self.create_widgets()
        # self.update_page()


    def clearLayout(self, layout=None) -> None:
        """ Clearing the current layout and its sublayouts
         :param layout: in function call None, but in recursion a sublayout can be referenced here
         """
        print("clear layout",flush=True)
        for i in range(len(self.non_basics)-1,-1,-1):
            item = self.non_basics[i]
            item.deleteLater()
            del self.non_basics[i]
        # if layout is None:
        #     layout = self.layout
        # while layout.count():
        #     item = layout.takeAt(0)
        #     widget = item.widget()
        #     if widget is not None:
        #         print(widget)
        #         widget.deleteLater()
        #     else:
        #         sublayout = item.layout()
        #         if sublayout:
        #             self.clearLayout(layout=sublayout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApplication()
    window.show()
    sys.exit(app.exec_())
