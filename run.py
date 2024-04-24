import sys

from source.ui_parts.StartWindow import StartWindow

sys.path.append('/source')
from source.permutation_group import permutation_group
import sys
from PyQt5.QtWidgets import QApplication



# p = permutation_group(4)
# p.get_all_standard_tableaus()
# p.print()

app = QApplication(sys.argv)
window = StartWindow()
window.show()
sys.exit(app.exec_())