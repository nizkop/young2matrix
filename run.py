import sys
import time
from PyQt5.QtWidgets import QApplication

from source.PermutationGroup import PermutationGroup
from source.texts.general_texts import get_general_text
from source.ui_parts.ApplicationWindows import ApplicationWindows


if __name__ == '__main__':
    if "-c" in sys.argv:#enable flag for console
        while True:
            permutation_no = input(get_general_text("input_line_command").replace(".","")+": ")
            try:
                try:
                    permutation_no = int(permutation_no)
                except:
                    raise Exception(get_general_text("warning_wrong_type"))
                if permutation_no <= 0:
                    raise Exception(get_general_text("warning_wrong_number"))#get_general_text("warning_no_group")
                break
            except Exception as e:
                print("\n", f"{str(e).replace('.','')}!", sep="")
        print(f"\n", get_general_text('download_start_info1'), permutation_no, get_general_text('download_start_info2').replace('\n\n','\n'), sep="")

        start_time = time.time()

        p = PermutationGroup(permutation_no)
        p.get_overview_pdf()

        print(f"Die Gesamtzeit für alle Funktionsaufrufe beträgt {-start_time+time.time():.4f} Sekunden.")
    else:
        app = QApplication(sys.argv)
        window = ApplicationWindows()
        window.show()
        sys.exit(app.exec_())




