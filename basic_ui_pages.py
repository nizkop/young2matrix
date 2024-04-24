import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QScrollArea, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.pages = {}
        self.create_page("Startseite", "Seite 1", "Seite 2", "Seite 3")

        self.set_page("Startseite")

    def create_page(self, *page_names):
        for page_name in page_names:
            page = QWidget()
            layout = QVBoxLayout(page)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)

            text_edit = QTextEdit()
            text_edit.setReadOnly(True)
            if page_name == "Seite 1":
                text_edit.setText("\n".join(["Dies ist ein langer, langer Text. Hier geht es um alles oder nichts."] * 10))
                text_edit.setHorizontalScrollBarPolicy(1)  # Qt::ScrollBarAlwaysOn
            elif page_name == "Seite 2":
                text_edit.setText("\n".join(["a ba c d"] * 20))

            scroll_area.setWidget(text_edit)

            layout.addWidget(scroll_area)

            button_layout = QHBoxLayout()
            back_to_home_btn = QPushButton("Zurück zur Startseite")
            back_to_home_btn.clicked.connect(lambda _, p="Startseite": self.set_page(p))

            button_layout.addWidget(back_to_home_btn)

            for target_page in page_names:
                if target_page != page_name and target_page != "Startseite":
                    goto_page_btn = QPushButton(f"Gehe zu {target_page}")
                    goto_page_btn.clicked.connect(lambda _, p=target_page: self.set_page(p))
                    button_layout.addWidget(goto_page_btn)

            layout.addLayout(button_layout)

            self.pages[page_name] = page
            self.layout.addWidget(page)

    def set_page(self, page_name):
        for name, page in self.pages.items():
            page.setVisible(name == page_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 640, 480)
    window.show()
    sys.exit(app.exec_())