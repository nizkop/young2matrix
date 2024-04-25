from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import matplotlib.pyplot as plt

from get_latex_canvas import add_formula

plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.preamble'] = r'''
\usepackage{amsmath}
\usepackage{tocloft}
\usepackage{physics}
\usepackage{breqn}
'''
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.scroll_layout = QVBoxLayout(self.central_widget)

        formula1 = r'\begin{array}{|c|} \hline 1\\ \cline{1-1} \end{array} \qquad \ket{ 1/2 \quad  -1/2 } = \left( + \beta _{1}\right)'
        formula = r'\begin{array}{c} a \\\hline \end{array} = \frac{1}{2} \quad \left( \alpha_{1} \qquad \beta \right) '
        add_formula(formula, self.scroll_layout)
        add_formula(formula1, self.scroll_layout)



#
# def add_formula(formula, scroll_layout: QVBoxLayout):
#         canvas = get_latex_canvas(formula)
#
#         scene = QGraphicsScene()
#         scene.addWidget(canvas)
#         graphics_view = QGraphicsView()
#         graphics_view.setScene(scene)
#         scroll_layout.addWidget(graphics_view)
# def get_latex_canvas(eq:str):
#     figure = plt.figure()
#     ax = figure.add_subplot(111)
#     ax.text(0.05, 0.5, rf"\[{eq}\]", horizontalalignment='left', verticalalignment='center', fontsize=20)
#     ax.axis('off')
#     figure.patch.set_facecolor('none')
#     plt.tight_layout(pad=0.2)

    # canvas = FigureCanvas(figure)
    # return canvas

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
