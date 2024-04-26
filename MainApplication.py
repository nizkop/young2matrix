
from matplotlib import pyplot as plt

from get_latex_canvas import get_latex_canvas, add_formula

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
        self.color = "lightgreen"
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

        self.setStyleSheet(f"background-color: {self.color};")

        self.current_page = 0
        self.pages = [
            {"name": "Startseite", "sign": "zurück zum Start", "index": 0, "function": self.load_main_page,
                    "parent": None, "buttons": [1, 3, 4, 5]},
            {"name": "Tableaus", "sign": "[1][2]", "index": 1, "function": self.load_tableau_page, "parent": 0,
                    "buttons": [0, 2, 3, 4]},
            {"name": "Ausmultiplizierte Tableaus", "sign": "ausmultiplizieren", "index": 2, "buttons": [0, 1, 3, 4],
                    "function": self.load_tableau_page_multiplied, "parent": 1},
            {"name": "Spin","sign": "σ", "index": 3, "function": self.load_spin_page, "parent": 0, "buttons": [0, 1, 4, 6]},
            {"name": "Raumfunktionen", "sign": "Φ", "index": 4, "function": self.load_spatial_page, "parent": 0,
                    "buttons": [0,1,3,7]},
            {"name": "Download", "sign": "⤓"# "⬇️" ↓ ⬇  ⤓
                    , "index": 5, "function": self.load_download, "parent": 0, "buttons": [0]},
            {"name": "Überlapp Spin", "sign": "<|> (σ)", "index": 6, "function": self.load_overlap_spin, "parent": 3,
                    "buttons": [0, 3, 7]},
            {"name": "Überlapp Raum", "sign": "<|> (Φ)", "index": 7, "function": self.load_overlap_spatial, "parent": 4,
                    "buttons": [0, 3, 6]},

        ]

        self.label = QLabel()
        self.label.setStyleSheet("background-color: transparent;")
        self.scroll_layout.addWidget(self.label)# inserts a bit of vertical space (thereby not in create_widget)

        self.create_widgets()


    def create_widgets(self):
        print("create widgets", flush=True)
        self.update_page() #content above buttons

        current_page_info = next((page_dict for page_dict in self.pages if page_dict.get("index") == self.current_page),
                                 None)

        button_layout = QHBoxLayout()  # horizontal layout (for buttons)
        for page_info in self.pages:
            if page_info["index"] != self.current_page and page_info["index"] in current_page_info["buttons"]:
                sign = f"zurück zu: {page_info['sign']}" \
                    if page_info["index"] == current_page_info["parent"] and self.current_page != 0 and current_page_info["parent"] != 0 \
                    else page_info["sign"]
                button = QPushButton(sign)
                button.setStyleSheet(f"background-color: {self.color};")
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
        # print("update_page", flush=True)
        formulas = [r"E = m \cdot c^ 2", r"\frac{1}{2}", "\\begin{array}{c}{1}\\end{array}", r"\bra{1}"]# test equations

        for formula in formulas:
            self.add_equation(formula)

    def add_equation(self, formula: str):
        """
        :param formula: latex-formatted equation, e.g. r"\frac{1}{2} \cdot \pi"
        """
        # print("add_equation", flush=True)
        canvas = get_latex_canvas(formula)
        self.scroll_layout.addWidget(canvas)
        self.non_basics.append(canvas)

        plt.close()


    def change_page(self, index: int):
        # print("change page",flush=True)
        self.clearLayout()
        self.current_page = index
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
