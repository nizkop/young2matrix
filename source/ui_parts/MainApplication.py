
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, \
    QScrollArea, QStatusBar

from source.ui_parts.get_latex_canvas import get_latex_canvas
from source.ui_parts.ui_pages import ui_pages, get_page_name
from source.ui_parts.settings.idea_config import update_language, get_language


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

        self.statusBar = QStatusBar()#information about button functions
        self.setStatusBar(self.statusBar)#(shown at the bottom of the screen)

        self.setStyleSheet(f"background-color: {self.color};")

        self.current_page = 0
        self.pages = [
            # TODO english names for pages ?
            {"sign": "start" if get_language()=="en" else "Start",
                    "index": ui_pages.START, "function": self.load_main_page, "parent": None,
                    "buttons": [ui_pages.TABLEAUS, ui_pages.SPIN, ui_pages.SPATIAL_FUNCTIONS, ui_pages.DOWNLOAD]},
            {"sign": "[1][2]", "index": ui_pages.TABLEAUS, "function": self.load_tableau_page, "parent": ui_pages.START,
                    "buttons": [ui_pages.START, ui_pages.MULTIPLIED_OUT_TABLEAUS, ui_pages.SPIN, ui_pages.SPATIAL_FUNCTIONS]},
            {"sign": "ausmultiplizieren" if get_language() == "de" else "multiply out", "index": ui_pages.MULTIPLIED_OUT_TABLEAUS,
                    "buttons": [ui_pages.START, ui_pages.TABLEAUS, ui_pages.SPIN, ui_pages.SPATIAL_FUNCTIONS],
                    "function": self.load_tableau_page_multiplied, "parent": ui_pages.TABLEAUS},
            {"sign": "σ", "index": ui_pages.SPIN, "function": self.load_spin_page, "parent": ui_pages.START,
                    "buttons": [ui_pages.START, ui_pages.TABLEAUS, ui_pages.SPATIAL_FUNCTIONS, ui_pages.OVERLAP_SPIN, ui_pages.HAMILTON_SPIN]},
            {"sign": "Φ", "index": ui_pages.SPATIAL_FUNCTIONS,
                    "function": self.load_spatial_page, "parent": ui_pages.START,
                    "buttons": [ui_pages.START, ui_pages.TABLEAUS, ui_pages.SPIN, ui_pages.OVERLAP_SPATIAL, ui_pages.HAMILTON_SPATIAL]},
            {"sign": "⤓"  # "⬇️" ↓ ⬇  ⤓
                    , "index": ui_pages.DOWNLOAD, "function": self.load_download, "parent": ui_pages.START, "buttons": [ui_pages.START]},
            {"sign": "<|> (σ)", "index": ui_pages.OVERLAP_SPIN,
                    "function": self.load_overlap_spin, "parent": ui_pages.SPIN,
                    "buttons": [ui_pages.START, ui_pages.SPIN, ui_pages.OVERLAP_SPATIAL, ui_pages.HAMILTON_SPIN]},
            {"sign": "<|> (Φ)", "index": ui_pages.OVERLAP_SPATIAL,
                    "function": self.load_overlap_spatial, "parent": ui_pages.SPATIAL_FUNCTIONS,
                    "buttons": [ui_pages.START, ui_pages.SPIN, ui_pages.OVERLAP_SPIN, ui_pages.HAMILTON_SPATIAL]},
            {"sign": "H (σ)" , "index": ui_pages.HAMILTON_SPIN, "function": self.load_hamilton_spin,
                    "parent": ui_pages.OVERLAP_SPIN, "buttons": [ui_pages.START, ui_pages.OVERLAP_SPIN, ui_pages.SPIN]},
            {"sign": "H (Φ)" , "index": ui_pages.HAMILTON_SPATIAL, "function": self.load_hamilton_spatial,
                    "parent": ui_pages.OVERLAP_SPATIAL, "buttons": [ui_pages.START, ui_pages.OVERLAP_SPIN, ui_pages.SPATIAL_FUNCTIONS]}
        ]
        for p in range(len(self.pages)):
            self.pages[p]["name"] = get_page_name(self.pages[p]["index"])

        self.label = QLabel()
        self.label.setStyleSheet("color: black;")
        self.label.setStyleSheet("background-color: transparent;")
        self.scroll_layout.addWidget(self.label)# inserts a bit of vertical space (thereby not in create_widget)

        self.create_language_buttons()

        self.create_widgets()


    def create_language_buttons(self) -> None:
        """ adding a button, that may change the language settings, to the top of the screen """
        if get_language() == "en":
            choice = "de"
            info ="change language to German"
        else:
            choice = "en"
            info = "Sprache zu Englisch ändern"

        self.language_button = QPushButton(choice)
        self.language_button.setStyleSheet(f"background-color: {self.color}; color: black")
        self.language_button.clicked.connect(lambda: self.set_language(choice))
        self.language_button.setFixedSize(30, 30)
        self.language_button.move(5, 5)
        self.scroll_layout.addWidget(self.language_button)

        self.language_button.setToolTip(info)
        self.language_button.enterEvent = lambda event, button= self.language_button: self.statusBar.showMessage( self.language_button.toolTip())
        self.language_button.leaveEvent = lambda event: self.statusBar.clearMessage()

    def set_language(self, language: str) -> None:
        """ updating the language (as it was changed by the user)
        :param language: abbreviation for the new language ('en' or 'de')
        """
        update_language(language)
        for p in range(len(self.pages)):# update pages names
            self.pages[p]["name"] = get_page_name(self.pages[p]["index"])
        self.language_button.deleteLater()
        self.create_language_buttons()
        self.open_page(self.current_page)


    def create_widgets(self) -> None:
        """
        setting up the buttons for the current page and linking them to following pages / information;
        because the buttons shall be at the bottom of the screen, first the creation of all other content of the page is initialized
        """
        # print("create widgets", flush=True)
        self.update_page() #content above buttons

        current_page_info = next((page_dict for page_dict in self.pages
                                  if page_dict.get("index").value == self.current_page), None)

        button_layout = QHBoxLayout()  # horizontal layout (for buttons)
        for page_info in self.pages:
            if page_info["index"].value != self.current_page and page_info["index"] in current_page_info["buttons"]:
                if page_info["index"] == current_page_info["parent"]:
                    sign = f"zurück zu: {page_info['sign']}" if get_language() == "de" else f"back to: {page_info['sign']}"
                else:
                    sign = page_info["sign"]

                button = QPushButton(sign)
                button.setStyleSheet(f"background-color: {self.color}; color: black")
                button.clicked.connect(lambda _, index=page_info["index"].value: self.open_page(index))
                button.setToolTip(page_info["name"])
                button.enterEvent = lambda event, button=button: self.statusBar.showMessage(button.toolTip())
                button.leaveEvent = lambda event: self.statusBar.clearMessage()

                button_layout.addWidget(button)
                self.non_basics.append(button)

        self.scroll_layout.addLayout(button_layout)
        self.non_basics.append(button_layout)

    def open_page(self, page_number:int) -> None:
        """
        to be implemented in sub-class
        :param page_number: number of the page to be opened
        :return: None
        """
        return self.change_page(page_number)

    def update_page(self) -> None:
        # print("update_page", flush=True)
        formulas = [r"E = m \cdot c^ 2", r"\frac{1}{2}", "\\begin{array}{c}{1}\\end{array}", r"\bra{1}"]# test equations

        for formula in formulas:
            self.add_equation(formula)

    def add_equation(self, formula: str) -> None:
        """
        adding a line with an equation to the current screen/page
        :param formula: latex-formatted equation, e.g. r"\frac{1}{2} \cdot \pi"
        """
        # print("add_equation", flush=True)
        canvas = get_latex_canvas(formula)
        self.scroll_layout.addWidget(canvas)
        self.non_basics.append(canvas)

        plt.close()


    def change_page(self, index: int) -> None:
        """
        changing a page by removing the old content and adding the new
        :param index: new page number
        """
        self.clearLayout()
        self.current_page = index
        self.create_widgets()


    def clearLayout(self) -> None:
        """ Clearing the current layout and its sublayouts """
        # print("clear layout",flush=True)
        for i in range(len(self.non_basics)-1,-1,-1):
            item = self.non_basics[i]
            item.deleteLater()
            del self.non_basics[i]
