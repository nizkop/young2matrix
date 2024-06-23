import matplotlib.pyplot as plt
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


def get_latex_canvas(eq:str, color:str) -> FigureCanvas:
    """
    building a suitable object for the ui from a string to display an equation
    :param eq: latex formatted equation including latex commands such as \cdot, \bra, \frac
    :param color: color of the text/lines/symbols in the equation (usually black)
    :return: figure of the equation
    """
    eq = eq.replace("_",r"\_")
    figure = plt.figure()
    ax = figure.add_axes([0, 0, 1, 1])
    if "rgb" in color:
        color = color.replace("rgb", "").replace("(", "").replace(")", "")
        r, g, b = map(int, color.split(','))
        color = "#{:02x}{:02x}{:02x}".format(r, g, b)
    ax.text(0.0, 0.5, rf"\[{eq}\]", color=color, horizontalalignment='left', verticalalignment='center', fontsize=20)
    ax.axis('off')
    figure.patch.set_facecolor('none')

    canvas = FigureCanvas(figure)
    plt.close(figure)
    return canvas


