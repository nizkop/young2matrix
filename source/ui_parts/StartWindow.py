import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QTableWidget, QTableWidgetItem



class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Permutationsgruppe")
        self.setGeometry(100, 100, 600, 400)#x position, x position, width, height

        self.layout = QVBoxLayout()
        self.setStyleSheet("background-color: lightgreen;")
        # self.add_equation("E=m\cdot c^2")
        self.adding_buttons()


    def adding_buttons(self):
        button1 = QPushButton("Seite 1")
        button1.clicked.connect(self.open_page1)
        self.layout.addWidget(button1)

    def add_equation(self, eq:str):
        """
        :param eq: latex-formatted equation, e.g.r"$\frac{1}{2} \cdot \pi$"
        """
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)
        self.ax.text(0.05, 0.5, # <- positioning
                     f"${eq}$", horizontalalignment='center', verticalalignment='center', fontsize=20)
        self.ax.axis('off')
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def open_page1(self):
        # Code für das Öffnen von Seite 1
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())
