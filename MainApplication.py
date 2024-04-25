
from matplotlib import pyplot as plt

from tst import get_latex_canvas, add_formula

# plt.rcParams['text.usetex'] = True
# plt.rcParams['text.latex.preamble'] = r'''
# \usepackage{mathtools}
# \usepackage{tocloft}
# \usepackage{physics}
# \usepackage{breqn}
# '''

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, \
    QScrollArea

class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.non_basics = []
        self.setWindowTitle("young2matrix")
        self.setGeometry(100, 100, 800, 600)

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
            {"name": "Startseite", "sign": "zurück zum Start", "index": 0, "function": self.load_main_page},
            {"name": "Tableaus", "sign": "[1][2]", "index": 1, "function": self.load_tableau_page},
            {"name": "Spin","sign": "σ", "index": 3, "function": self.load_spin_page},
            {"name": "Raumfunktionen", "sign": "Φ", "index": 3, "function": self.load_spatial_page},
            {"name": "Download", "sign": "⤓"# "⬇️" ↓ ⬇  ⤓
                , "index": 4, "function": self.test_page}
        ]

        self.label = QLabel()
        self.label.setStyleSheet("background-color: transparent;")
        self.scroll_layout.addWidget(self.label)# inserts a bit of vertical space (thereby not in create_widget)

        self.create_widgets()


    def create_widgets(self):
        print("create widgets", flush=True)
        self.update_page() #content above buttons

        button_layout = QHBoxLayout()  # horizontal layout (for buttons)

        for page_info in self.pages: # for i, (text, _) in enumerate(self.pages):
            if page_info["index"] != self.current_page:
                button = QPushButton(page_info["sign"])
                button.setStyleSheet("background-color: lightgreen;")
                button.clicked.connect(lambda _, index=page_info["index"]: self.open_page(index))
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
        formulas = [r"E = m \cdot c^ 2", r"\frac{1}{2}", "\\begin{array}{c}{1}\\end{array}", r"\bra{1}"]# test equations

        for formula in formulas:
            self.add_equation(formula)

    def add_equation(self, formula: str):
        """
        :param formula: latex-formatted equation, e.g. r"\frac{1}{2} \cdot \pi"
        """
        print("add_equation", flush=True)
        # plt.rcParams['text.usetex'] = True
        # plt.rcParams['text.latex.preamble'] = r'''
        # \usepackage{mathtools}
        # \usepackage{tocloft}
        # \usepackage{physics}
        # \usepackage{breqn}
        # '''
        #
        # figure = plt.figure()
        # ax = figure.add_subplot(111)
        # ax.text(0.05, 0.5, rf"\[{formula}\]", horizontalalignment='left', verticalalignment='center', fontsize=20)
        # ax.axis('off')
        # figure.patch.set_facecolor('none')
        # plt.tight_layout(pad=0.2)
        #
        # # bbox = ax.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
        # # width = int(bbox.width * figure.dpi)
        # # height = int(bbox.height * figure.dpi/3)
        # canvas = FigureCanvas(figure)
        # # canvas.setFixedSize(width, height)

        canvas = get_latex_canvas(formula)
        add_formula(formula, self.scroll_layout)
        # scene = QGraphicsScene()
        # scene.addWidget(canvas)
        # graphics_view = QGraphicsView()
        # graphics_view.setScene(scene)
        # self.scroll_layout.addWidget(graphics_view)
        # self.scroll_layout.addWidget(widget, alignment=Qt.AlignLeft)

        # self.scroll_layout.addWidget(canvas, alignment=Qt.AlignLeft)
        self.non_basics.append(canvas)

        plt.close()

        # try:
        #     figure.tight_layout(pad=0.2)
        #     figure.canvas.draw()
        # except:
        #     print("problematic equation", [formula], flush=True)
        #     self.scroll_layout.addWidget(canvas, alignment=Qt.AlignLeft)
        #     # latex_text = ax.texts[0].get_text()
        #     # with open('rendered_text.tex', 'w') as f:
        #     #     f.write(latex_text)
        #     # plt.show()
        #     eq = r"nicht \quad darstellbar"
        #     return self.add_equation(eq)

    def change_page(self, index: int):
        print("change page",flush=True)
        self.current_page = index
        self.clearLayout()
        self.create_widgets()
        # self.update_page()


    def clearLayout(self) -> None:
        """ Clearing the current layout and its sublayouts """
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



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainApplication()
#     window.show()
#     sys.exit(app.exec_())
