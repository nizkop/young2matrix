import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon



class PageYoungTableaus(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)#main page
        self.label = QLabel("Standard Young Tableaus")
        parent.layout.addWidget(self.label)
        self.back_button = QPushButton("zurück")
        self.back_button.clicked.connect(parent.back_to_start)
        parent.layout.addWidget(self.back_button)