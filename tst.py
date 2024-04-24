import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap, QPainter, QPalette, QColor
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hauptstartseite")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        self.setStyleSheet("background-color: lightgreen;")

        self.current_page = 0
        self.pages = [
            ("Seite 1", r"$\sum_{i=1}^{n} i^2$"),
            ("Seite 2", r"$e^{i\pi} + 1 = 0$")
        ]

        self.create_widgets()

    def create_widgets(self):
        self.label = QLabel()
        self.label.setStyleSheet("background-color: lightgreen;")
        self.scroll_layout.addWidget(self.label)
        self.update_page()

        button_layout = QVBoxLayout()

        for i, (text, _) in enumerate(self.pages):
            button = QPushButton(text)
            button.setStyleSheet("background-color: lightgreen;")
            button.clicked.connect(lambda _, i=i: self.change_page(i))
            button_layout.addWidget(button)

        self.scroll_layout.addLayout(button_layout)

    def update_page(self):
        _, formula = self.pages[self.current_page]
        fig = Figure(figsize=(4, 3))
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, formula, ha='center', va='center', fontsize=14)
        ax.axis('off')

        canvas = FigureCanvas(fig)
        canvas.draw()
        pixmap = QPixmap(canvas.size())
        pixmap.fill(QColor(canvas.palette().color(QPalette.Window)))
        painter = QPainter(pixmap)
        canvas.render(painter)
        painter.end()

        self.label.setPixmap(pixmap)

    def change_page(self, index):
        self.current_page = index
        self.update_page()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApplication()
    window.show()
    sys.exit(app.exec_())
