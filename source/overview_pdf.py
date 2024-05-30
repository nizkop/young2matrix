import locale
from datetime import date
from typing import Union
from pylatex import Document, Section, Math, Command, Package, Subsection, Center
from pylatex.utils import NoEscape

from source.texts.general_texts import get_general_text
from source.ui_parts.settings.language_choices import language_choices
from source.ui_parts.settings.settings_config import get_language


class overview_pdf(object):
    def __init__(self):
        self.permutation_group:int=0
        self.file_type:str = "pdf"

        self.language = get_language()
        if get_language() == "de":
            locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')# changes name of month into german version

        self.doc = Document(documentclass='article', document_options=['fleqn']) # left alignment for equations
        self.doc.packages.append(Package('geometry',
                 options=['a4paper', 'left=2cm', 'right=2cm', 'top=2cm', 'bottom=2cm']))
        self.doc.preamble.append(Package("babel", options=r'ngerman'))
        self.doc.preamble.append(Package("tocloft"))
        self.doc.preamble.append(NoEscape(r"\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}   % activating dots in table of contents"))
        self.doc.preamble.append(Package("physics"))
        self.doc.preamble.append(Package("breqn"))# for dmath command

        self.doc.append(Command('noindent'))
        self.doc.packages.append(Package('setspace', options=['doublespacing']))

        self.add_title_page()
        # self.add_header()

    def add_title_page(self):
        self.doc.append(Command('thispagestyle', 'empty'))

        with self.doc.create(Center()):
            self.doc.append(Command('vspace*', '4cm'))
            self.doc.append(Command('Huge', ""))
            for line in get_general_text("pdf_title").split("\n"):
                self.doc.append(line)
                self.doc.append(Command(r'\ '))
            self.doc.append(Command('vspace', '1cm'))
            self.doc.append(Command('Large', f"{get_general_text('permutation_part_title')}: {self.permutation_group}"))
            self.doc.append(Command(r'\ '))
            self.doc.append(Command('vspace', '4cm'))
            if self.language == language_choices.en.name:
                self.doc.append(Command('Large', date.today().strftime('%B %d, %Y')))
            else:#default
                print(self.language, language_choices.en.name)
                self.doc.append(Command('Large', date.today().strftime('%d. %B %Y')))

        self.newpage()
        self.doc.append(Command('setcounter', arguments=['page', '1']))

    # def add_header(self):
    #     self.doc.append(Command('pagestyle', 'headings'))



    def save(self, title:str) -> None:
        """
        '.pdf' is added automatically
        :param title: name of the to-be-generated pdf file
        :return:
        """
        self.doc.append(Command('newpage'))  # Seite umbrechen
        self.doc.append(Command('tableofcontents'))
        self.doc.generate_pdf(title, clean_tex=True)

    def add_information(self, additional_info:str) -> None:
        """ adding text to the current chapter of the pdf """
        self.doc.append(NoEscape(additional_info))

    def add_section(self, sec_title:str, content:str, layer:int=0) -> None:
        """ adding a new section/chapter to the pdf
        :param sec_title: name of the new chapter
        :param content: text in the new chapter
        :param layer: chapter hierarchy number (0 = highest layer)
                      -> indicating whether the chapter is a subchapter to prior chapters, or not
        """
        if layer == 0:
            with self.doc.create(Section(sec_title)):
                if len(content) > 0:
                    self.doc.append(NoEscape(content))
        elif layer == 1:
            with self.doc.create(Subsection(sec_title)):
                if len(content) > 0:
                    self.doc.append(NoEscape(content))
        else:
            return

    def get_latex_formula(self, formula_text:str, inline:bool = False) -> Union[Math, NoEscape]:
        """
        adding a latex formatted equation to the pdf
        :param: latex equation including latex commands
        :inline: boolean indicating whether the latex formula is short and does not need a separate line or not
        :return: pdf/latex math object, that will be rendered into the pdf
        """
        if not inline: # euqation might be longer
            return NoEscape(r"\begin{dmath*}"+rf"{formula_text}"+r"\end{dmath*}")
        return Math(data=[NoEscape(rf"{formula_text}")], inline=inline)

    def add_latex_formula(self, formula_text:str, inline:bool = False) -> None:
        """
        :param formula_text: latex-equation
        :param inline: whether the equation should be written in the same line as content before (False)
                       or if it should get a line for itself (True)
        :return:
        """
        self.doc.append(self.get_latex_formula(formula_text=formula_text, inline=inline))
        # a = np.array([[100, 10, 20]]).T
        # M = np.matrix([[2, 3, 4],
        #                [0, 0, 1],
        #                [0, 0, 2]])
        # self.doc.append(Math(data=[Matrix(M), Matrix(a), '=', Matrix(M * a)]))

    def newpage(self) -> None:
        """ adding a page break """
        self.doc.append(Command('newpage'))

    def vspace(self) -> None:
        """ adding vertical space after the current line """
        self.doc.append(Command('vspace', '0.25cm'))


if __name__ == '__main__':
    o = overview_pdf()
    o.add_information("here it goes")
    o.add_latex_formula(NoEscape(r"E = m \cdot c^2"))
    o.add_information("bla bla bla")
    o.save("bla")