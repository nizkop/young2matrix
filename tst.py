import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QVBoxLayout, QGraphicsScene, QGraphicsView
# from matplotlib_inline.backend_inline import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

plt.rcParams['text.usetex'] = True
plt.rcParams['text.latex.preamble'] = r'''
\usepackage{amsmath}
%\usepackage{mathtools}
\usepackage{tocloft}
\usepackage{physics}
\usepackage{breqn}
'''

# plt.imshow(np.random.randn(100, 100))
# plt.title('This is a test')
# plt.xlabel(r'$x\cdot \bra{E}$')
# plt.ylabel(r'$\text{y}$')
# plt.savefig('test.pdf')


# test 2


def get_latex_canvas(eq:str):
    eq = eq.replace("_",r"\_")

    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.text(0.05, 0.5, rf"\[{eq}\]", horizontalalignment='left', verticalalignment='center', fontsize=20)
    ax.axis('off')
    figure.patch.set_facecolor('none')
    # plt.tight_layout(pad=0.2)

    canvas = FigureCanvas(figure)
    plt.show()
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


get_latex_canvas(r"\bra{E}\ket{x} = \frac{1}{2} = \begin{array}{|c|} 1 \\ \hline \end{array}")