from typing import Union
from pylatex import Document, Section, Math, Command, Package, Subsection
from pylatex.utils import NoEscape


class overview_pdf(object):
    def __init__(self):
        self.permutation_group:int=0
        self.file_type:str = "pdf"

        self.doc = Document(documentclass='article', document_options=['fleqn']) # left alignment for equations
        self.doc.packages.append(Package('geometry',
                 options=['a4paper', 'left=2cm', 'right=2cm', 'top=2cm', 'bottom=2cm']))
        self.doc.preamble.append(Package("babel", options=r'ngerman'))
        self.doc.preamble.append(Package("tocloft"))
        self.doc.preamble.append(NoEscape(r"\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}   % activating dots in table of contents"))
        self.doc.preamble.append(Package("physics"))
        self.doc.preamble.append(Package("breqn"))# for dmath command

        self.doc.append(Command('noindent'))

    def save(self, title:str) -> None:
        """
        '.pdf' is added automatically
        :param title:
        :return:
        """
        self.doc.append(Command('newpage'))  # Seite umbrechen
        self.doc.append(Command('tableofcontents'))
        self.doc.generate_pdf(title, clean_tex=True)

    def add_information(self, additional_info:str) -> None:
        self.doc.append(NoEscape(additional_info))

    def add_section(self, sec_title:str, content:str, layer:int=0) -> None:
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
        self.doc.append(Command('newpage'))

    def vspace(self) -> None:
        self.doc.append(Command('vspace', '0.25cm'))


if __name__ == '__main__':
    o = overview_pdf()
    o.add_information("here it goes")
    o.add_latex_formula(NoEscape(r"E = m \cdot c^2"))
    o.add_information("bla bla bla")
    o.save("bla")