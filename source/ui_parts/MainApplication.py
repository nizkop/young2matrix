from abc import abstractmethod
from typing import Union, Dict, List
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QVBoxLayout, QSpacerItem, QSizePolicy, QHBoxLayout, QWidget, QLayout
from qtpy import QtCore

from source.settings.GLOBALS import BUTTON_SIZE, FONT_SIZE, MARGIN_TOP_Y
from source.settings.settings_config import get_language, get_color
from source.ui_parts.LayoutAndButtonApplication import LayoutAndButtonApplication
from source.ui_parts.canvas_equations.determine_height_of_equation import determine_height_of_equation
from source.ui_parts.canvas_equations.get_latex_canvas import get_latex_canvas
from source.ui_parts.canvas_equations.get_max_number_of_signs_in_equation import fit_length_to_width
from source.ui_parts.get_basic_formatting_for_layout_part import format_layout_part
from source.ui_parts.small_basic_parts.get_basic_label import get_basic_label
from source.ui_parts.small_basic_parts.get_basic_push_button import get_basic_push_button
from source.settings.LanguageChoices import LanguageChoices
from source.ui_parts.UiPages import UiPages, get_page_name



class MainApplication(LayoutAndButtonApplication):
    """ class in-between
    - LayoutAndButtonApplication (which is more general)
    - and ApplicationWindows (which
     -> here a basic structure of the pages and methods for changing them are given
     """

    def __init__(self):
        super().__init__()
        self.buttons = []
        self.setWindowTitle("young2matrix")

        self.current_page:int = 0
        self.pages: List[Dict] = [
            {"sign": "start" if get_language() == LanguageChoices.en.name else "Start",
                    "index": UiPages.START, "function": self.load_main_page, "parent": None,
                    "buttons": [UiPages.TABLEAUS, UiPages.SPIN, UiPages.SPATIAL_FUNCTIONS, UiPages.DOWNLOAD]},
            {"sign": "[1][2]", "index": UiPages.TABLEAUS, "function": self.load_tableau_page, "parent": UiPages.START,
                    "buttons": [UiPages.START, UiPages.MULTIPLIED_OUT_TABLEAUS, UiPages.SPIN, UiPages.SPATIAL_FUNCTIONS]},
            {"sign": "ausmultiplizieren" if get_language() == LanguageChoices.de.name else "multiply out",
                    "index": UiPages.MULTIPLIED_OUT_TABLEAUS,
                    "buttons": [UiPages.START, UiPages.TABLEAUS, UiPages.SPIN, UiPages.SPATIAL_FUNCTIONS],
                    "function": self.load_tableau_page_multiplied, "parent": UiPages.TABLEAUS},
            {"sign": "σ", "index": UiPages.SPIN, "function": self.load_spin_page, "parent": UiPages.START,
                    "buttons": [UiPages.START, UiPages.TABLEAUS, UiPages.SPATIAL_FUNCTIONS,
                                UiPages.OVERLAP_SPIN, UiPages.HAMILTON_SPIN]},
            {"sign": "Φ", "index": UiPages.SPATIAL_FUNCTIONS,
                    "function": self.load_spatial_page, "parent": UiPages.START,
                    "buttons": [UiPages.START, UiPages.TABLEAUS, UiPages.SPIN,
                                UiPages.OVERLAP_SPATIAL, UiPages.HAMILTON_SPATIAL]},
            {"sign": "⤓"  # "⬇️" ↓ ⬇  ⤓
                    , "index": UiPages.DOWNLOAD, "function": self.load_download,
                    "parent": UiPages.START, "buttons": [UiPages.START]},
            {"sign": "<|> (σ)", "index": UiPages.OVERLAP_SPIN,
                    "function": self.load_overlap_spin, "parent": UiPages.SPIN,
                    "buttons": [UiPages.START, UiPages.SPIN, UiPages.OVERLAP_SPATIAL, UiPages.HAMILTON_SPIN]},
            {"sign": "<|> (Φ)", "index": UiPages.OVERLAP_SPATIAL,
                    "function": self.load_overlap_spatial, "parent": UiPages.SPATIAL_FUNCTIONS,
                    "buttons": [UiPages.START, UiPages.SPATIAL_FUNCTIONS, UiPages.OVERLAP_SPIN, UiPages.HAMILTON_SPATIAL]},
            {"sign": "H (σ)" , "index": UiPages.HAMILTON_SPIN, "function": self.load_hamilton_spin,
                    "parent": UiPages.OVERLAP_SPIN,
                    "buttons": [UiPages.START, UiPages.OVERLAP_SPIN, UiPages.OVERLAP_SPATIAL, UiPages.SPIN]},
            {"sign": "H (Φ)" , "index": UiPages.HAMILTON_SPATIAL, "function": self.load_hamilton_spatial,
                    "parent": UiPages.OVERLAP_SPATIAL, "buttons": [UiPages.START, UiPages.OVERLAP_SPATIAL,
                                                                   UiPages.OVERLAP_SPIN, UiPages.SPATIAL_FUNCTIONS]}
        ]
        for p in range(len(self.pages)):
            self.pages[p]["name"] = get_page_name(self.pages[p]["index"])

        self.update_page()
        self.create_widgets()

    def create_widgets(self) -> None:
        """
        AFTER CONTENT IS ADDED!
        setting up the buttons for the current page and linking them to following pages / information;
        because the buttons shall be at the bottom of the screen, first the creation of all other content of the page is initialized
        """
        current_page_info = next((page_dict for page_dict in self.pages
                                  if page_dict.get("index").value == self.current_page), None)
        self.buttons = []#remove prior buttons from fast access
        button_layout = QHBoxLayout()  # horizontal layout (for buttons)
        for page_info in self.pages:
            if page_info["index"].value != self.current_page and page_info["index"] in current_page_info["buttons"]:
                if page_info["index"] == current_page_info["parent"]:
                    sign = f"zurück zu: {page_info['sign']}" if get_language() == LanguageChoices.de.name \
                            else f"back to: {page_info['sign']}"
                else:
                    sign = page_info["sign"]

                button = get_basic_push_button(sign)
                button.setFixedHeight(BUTTON_SIZE)
                format_layout_part(button)#f"background-color: {self.color.value['background']}; " +
                                                   # f"color: {self.color.value['text']}; font-weight: bold; " +
                                                   # f"font-size: {self.button_font_size}pt;")
                button.clicked.connect(lambda _, index=page_info["index"].value: self.open_page(index))
                button.setToolTip(f"<span style='font-size:{FONT_SIZE}pt;'>{page_info['name']}</span>")
                name = page_info['name']  # Freeze current name (so that not the last triggerer counts for every event)
                # noinspection PyUnresolvedReferences
                button.enterEvent = lambda event, button=button, name=name: self.change_status_message(name)
                button.leaveEvent = lambda event: self.change_status_message()
                button_layout.addWidget(button)
                self.buttons.append(button)

        # ensuring that buttons are at the bottom:
        spacer = QSpacerItem(0, self.spacer_height, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.scroll_layout.addItem(spacer)
        # adding width-limited button panel to layout:
        self.button_layout_widget = QWidget()
        self.button_layout_widget.setLayout(button_layout)
        self.button_layout_widget.setFixedSize(self.width()-MARGIN_TOP_Y*4,
                                          button_layout.sizeHint().height())
        self.scroll_layout.addWidget(self.button_layout_widget)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        adjusting the widths of all current buttons
        """
        super().resizeEvent(event)#move help button to the right side
        self.button_layout_widget.setFixedWidth(self.width() - MARGIN_TOP_Y * 4)

    def set_ui_label(self, header: str = None, content: str = None, spacing: bool = True) -> None:
        if header and content:
            text = f"<b>{header}</b><p>{content}</p>"
        elif header:
            text = f"<b>{header}</b>"
        elif content:
            text = f"<p>{content}</p>"
            spacing=False
        else:
            raise Exception("A label needs some kind of content.")
        if spacing is True:
            text += "<br>"
        self.scroll_layout.addWidget(get_basic_label(text, allowed_width=self.width()))

    def add_equation(self, formula: str, add_indent=False) -> None:
        """
        adding a line with an equation to the current screen/page
        :param formula: latex-formatted equation, e.g. r"\frac{1}{2} \cdot \pi"
        """
        # get equation as picture:
        canvas = get_latex_canvas(eq=formula, color=get_color()["text"])

        # find needed size (so the equation is not clipped):
        height = determine_height_of_equation(formula)
        width = fit_length_to_width(formula)
        canvas.setFixedSize(QtCore.QSize(width, height))

        # align equation with a fixed margin to the left side:
        line = QHBoxLayout()
        line.setAlignment(Qt.AlignLeft)
        if add_indent:
            spacer = QSpacerItem(self.spacer_height*2, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        else:
            spacer = QSpacerItem(self.spacer_height, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        line.addItem(spacer)
        line.addWidget(canvas)

        # adding to view:
        self.scroll_layout.addLayout(line)

    def change_page(self, index: int) -> None:
        """
        changing a page by removing the old content and adding the new
        :param index: new page number
        """
        self.clear_screen()
        self.current_page = index
        if self.current_page != UiPages.DOWNLOAD.value:
            self.update_page()
            self.create_widgets()
        else:
            self.update_page()

    def clear_screen(self) -> None:
        """ Clearing the current layout and its sublayouts """
        self.clear_layout()
        self.create_settings_button()
        self.create_help_button()

    def clear_layout(self, layout: Union[QHBoxLayout, QVBoxLayout, QLayout, None]=None) -> None:
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


    ###   abstract methods: to be implemented in sub-class  ###########################################################################
    @abstractmethod
    def open_page(self, page_number:int) -> None:
        pass
    @abstractmethod
    def update_page(self) -> None:
        pass
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