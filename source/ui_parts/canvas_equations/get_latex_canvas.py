import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QVBoxLayout

# NOT: from matplotlib_inline.backend_inline import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.preamble'] = r'''
\usepackage{amsmath}
%\usepackage{mathtools}
\usepackage{tocloft}
\usepackage{physics}
\usepackage{breqn}
'''


def get_latex_canvas(eq:str, color:str) -> FigureCanvas:#todo scroll/size
    """
    building a suitable object for the ui from a string to display an equation
    :param eq: latex formatted equation including latex commands such as \cdot, \bra, \frac
    :param color: color of the text/lines/symbols in the equation (usually black)
    :return: figure of the equation
    """
    eq = eq.replace("_",r"\_")
    # width=max((eq.count("\n")+1)*0.5,2.0)
    # height=200
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.text(0.05, 0.5, rf"\[{eq}\]", color=color, horizontalalignment='left', verticalalignment='center', fontsize=20)
    ax.axis('off')
    # figure.patch.set_facecolor('none')
    plt.tight_layout(pad=0.2)#centering horizontally

    # print(figure, figure.bbox )
    canvas = FigureCanvas(figure)
    # plt.show()
    plt.close(figure)
    return canvas




def add_formula(formula, scroll_layout: QVBoxLayout):
        canvas = get_latex_canvas(formula)
        scroll_layout.addWidget(canvas)

        # scene = QGraphicsScene()
        # scene.addWidget(canvas)
        # graphics_view = QGraphicsView()
        # graphics_view.setScene(scene)
        # scroll_layout.addWidget(graphics_view)


if __name__ == '__main__':
    get_latex_canvas(r"\bra{E}\ket{x} = \frac{1}{2} = \begin{array}{|c|} 1 \\ \hline \end{array}")