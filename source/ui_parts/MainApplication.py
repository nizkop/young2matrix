from abc import abstractmethod
from typing import Union, Dict, List
from PyQt5.QtWidgets import QVBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QHBoxLayout, QWidget
from qtpy import QtCore

from source.ui_parts.LayoutAndButtonApplication import LayoutAndButtonApplication
from source.ui_parts.canvas_equations.determine_height_of_equation import determine_height_of_equation
from source.ui_parts.canvas_equations.get_latex_canvas import get_latex_canvas
from source.ui_parts.canvas_equations.get_max_number_of_signs_in_equation import fit_length_to_width
from source.ui_parts.settings.language_choices import language_choices
from source.ui_parts.ui_pages import ui_pages, get_page_name
from source.ui_parts.settings.idea_config import get_language


class MainApplication(LayoutAndButtonApplication):
    """ class in-between
    - LayoutAndButtonApplication (which is more general)
    - and ApplicationWindows (which
     -> here a basic structure of the pages and methods for changing them are given """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("young2matrix")

        self.current_page:int = 0
        self.pages: List[Dict] = [
            {"sign": "start" if get_language()== language_choices.en.name else "Start",
                    "index": ui_pages.START, "function": self.load_main_page, "parent": None,
                    "buttons": [ui_pages.TABLEAUS, ui_pages.SPIN, ui_pages.SPATIAL_FUNCTIONS, ui_pages.DOWNLOAD]},
            {"sign": "[1][2]", "index": ui_pages.TABLEAUS, "function": self.load_tableau_page, "parent": ui_pages.START,
                    "buttons": [ui_pages.START, ui_pages.MULTIPLIED_OUT_TABLEAUS, ui_pages.SPIN, ui_pages.SPATIAL_FUNCTIONS]},
            {"sign": "ausmultiplizieren" if get_language() == language_choices.de.name else "multiply out", "index": ui_pages.MULTIPLIED_OUT_TABLEAUS,
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

        self.create_widgets()

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
                    sign = f"zurück zu: {page_info['sign']}" if get_language() == language_choices.de.name else f"back to: {page_info['sign']}"
                else:
                    sign = page_info["sign"]

                button = QPushButton(sign)
                button.setStyleSheet(f"background-color: {self.color.value['background']}; color: {self.color.value['text']}; font-weight: bold;")
                button.clicked.connect(lambda _, index=page_info["index"].value: self.open_page(index))
                button.setToolTip(page_info["name"])
                button.enterEvent = lambda event, button=button: self.change_status_message(button.toolTip())
                button.leaveEvent = lambda event: self.change_status_message()

                button_layout.addWidget(button)

        # ensuring that buttons are at the bottom:
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.scroll_layout.addItem(spacer)
        # adding width-limited button panel to layout:
        button_layout_widget = QWidget()
        button_layout_widget.setLayout(button_layout)
        button_layout_widget.setFixedSize(self.width()-self.margin_x*4, button_layout.sizeHint().height())
        self.scroll_layout.addWidget(button_layout_widget)

    def set_ui_label(self, header: str = None, content: str = None, spacing:bool=True) -> None:
        if header and content:
            text = f"<b>{header}</b><p>{content}</p>"
        elif header:
            text = f"<b>{header}</b>"
        elif content:
            text = f"<p>{content}</p>"
            spacing=False
        else:
            raise Exception("Label needs some kind of content")
        if spacing is True:
            text += "<br>"
        label = QLabel(text)
        label.setTextFormat(Qt.RichText)#enable html formatting
        label.setWordWrap(True)
        label.setMaximumWidth(self.width())
        label.setStyleSheet(f"color: {self.color.value['text']};")
        self.scroll_layout.addWidget(label)

    def add_equation(self, formula: str) -> None:
        """
        adding a line with an equation to the current screen/page
        :param formula: latex-formatted equation, e.g. r"\frac{1}{2} \cdot \pi"
        """
        # print("\nadd_equation", formula, flush=True)
        canvas = get_latex_canvas(eq=formula, color=self.color.value["text"])

        height = determine_height_of_equation(formula)
        width = fit_length_to_width(formula)

        # print(width, get_max_number_of_signs_in_equation(eq=formula))
        canvas.setFixedSize(QtCore.QSize(width, height))
        self.scroll_layout.addWidget(canvas)
        # plt.close()

    def change_page(self, index: int) -> None:
        """
        changing a page by removing the old content and adding the new
        :param index: new page number
        """
        self.clear_screen()
        self.current_page = index
        self.create_widgets()

    def clear_screen(self) -> None:
        """ Clearing the current layout and its sublayouts """
        self.clear_layout()
        self.create_settings_button()
        self.create_help_button()

    def clear_layout(self, layout: Union[QHBoxLayout, QVBoxLayout, None]=None) -> None:
        if layout == None:
            layout = self.scroll_layout

        while layout.count():
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    sublayout = item.layout()
                    if sublayout:
                        self.clear_layout(sublayout)


    ###   abstract methods   ###########################################################################
    @abstractmethod
    def open_page(self, page_number:int) -> None:
        """
        to be implemented in sub-class
        :param page_number: number of the page to be opened
        :return: None
        """
        return self.change_page(page_number)

    @abstractmethod
    def update_page(self) -> None:
        # print("update_page", flush=True)
        formulas = [r"E = m \cdot c^ 2", r"\frac{1}{2}", "\\begin{array}{c}{1}\\end{array}", r"\bra{1}"]# test equations

        for formula in formulas:
            self.add_equation(formula)

    @abstractmethod
    def load_main_page(self):
        pass
    @abstractmethod
    def load_tableau_page(self):
        pass
    @abstractmethod
    def load_spatial_page(self):
        pass
    @abstractmethod
    def load_spin_page(self):
        pass
    @abstractmethod
    def load_download(self):
        pass
    @abstractmethod
    def load_overlap_spatial(self):
        pass
    @abstractmethod
    def load_overlap_spin(self):
        pass
    @abstractmethod
    def load_hamilton_spatial(self):
        pass
    @abstractmethod
    def load_hamilton_spin(self):
        pass