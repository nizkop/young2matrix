import numpy as np
from pylatex import Document, Section, Math, Matrix
from pylatex.base_classes import Environment
from pylatex.utils import italic, NoEscape


class overview_pdf(object):
    def __init__(self):
        self.permutation_group:int=0
        self.file_type:str = "pdf"

        self.doc = Document()

    def save(self, title: str) -> None:
        """
        '.pdf' is added automatically
        :param title:
        :return:
        """
        self.doc.generate_pdf(title, clean_tex=True)

    # def add_information(self, additional_info: str)->None:
    #     pass

    def add_information(self, additional_info: str) -> None:
        self.doc.append(additional_info)

    def add_section(self, sec_title:str, content:str):
        with self.doc.create(Section(sec_title)):
            self.doc.append(content)

    def add_latex_formula(self, formula_text: str, inline:bool = True) -> None:
        """
        :param formula_text: latex-equation
        :param inline: whether the equation should be written in the same line as content before (False)
                       or if it should get a line for itself (True)
        :return:
        """
        self.doc.append(Math(data=[NoEscape(rf"{formula_text}")], inline=inline))
        # a = np.array([[100, 10, 20]]).T
        # M = np.matrix([[2, 3, 4],
        #                [0, 0, 1],
        #                [0, 0, 2]])
        # self.doc.append(Math(data=[Matrix(M), Matrix(a), '=', Matrix(M * a)]))


if __name__ == '__main__':
    o = overview_pdf()
    o.add_information("here it goes")
    o.add_latex_formula(NoEscape(r"E = m \cdot c^2"))
    o.add_information("bla bla bla")
    o.save("bla")