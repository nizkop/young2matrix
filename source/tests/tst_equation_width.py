from source.ui_parts.canvas_equations.get_max_number_of_signs_in_equation import get_max_number_of_signs_in_equation

tests = [
    {"eq": r"\sqrt{2}", "expected_length": 2, "width": 50},
    {"eq": r"\left(12\right)", "expected_length": 4, "width": 70},#
    {"eq": r"\frac{1}{2}", "expected_length": 1, "width": 50},
    {"eq": r"\frac{2\cdot a_1}{2}", "expected_length": 6, "width": 90},
    {"eq": r"α", "expected_length": 1},
    {"eq": r"\alpha", "expected_length": 1},
    {"eq": r"\begin{array}{|c|} \hline 1\\ \cline{1-1} 2\\ \cline{1-1} \end{array}", "expected_length": 1+8, "width": 45},
    {"eq": r"\begin{array}{|c|} \hline123\\ \cline{1-1} 2\\ \cline{1-1} \end{array}", "expected_length": 3+8, "width": 90},
    {"eq": r"\begin{array}{|c|} \hline 1\\ \cline{1-1} 2\\ \cline{1-1} 3 \\ \cline{1-1} \end{array}", "expected_length": 1+8, "width": 48},
    {"eq": r" \begin{array}{|c|} \hline 1\\ \cline{1-1} \end{array} \quad \left( + a_{1}\right) ", "expected_length": 8+8, "width": 160},
]



for trial in tests:
    no = get_max_number_of_signs_in_equation(trial["eq"])
    if no < trial["expected_length"]-1 or no > trial["expected_length"]+1:
        raise Exception(f"unfitting test case: {no} vs. {trial}")