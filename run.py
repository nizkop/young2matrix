import sys
from PyQt5.QtWidgets import QApplication
from source.ui_parts.ApplicationWindows import ApplicationWindows



app = QApplication(sys.argv)
window = ApplicationWindows()
window.show()
sys.exit(app.exec_())
