import copy
import math


def get_max_number_of_signs_in_equation(eq:str) -> int:
    formula = copy.deepcopy(eq)
    # print("get_max_number_of_signs_in_equation", formula)

    # formula = formula.replace(" ", "")# is displayed in UI!
    formula = formula.replace(r"\\hline","")
    formula = formula.replace(r"\\quad","p").replace(r"\\qquad","pp")#placeholders
    formula = formula.replace(r"\\cdot", "m")
    if len(formula) == 0:
        return 0
    # reduce frac to longest part:
    while "frac" in formula:
        index = formula.find(r"\frac")
        formula_before = formula[:index]
        formula_after = formula[index+len(r"\frac")+1:]
        counter = formula[index+len(r"\frac")+1:]
        index_first_end = counter.find("}")
        counter = counter[:index_first_end] #.replace("{","").replace("}","")
        denominator = formula_after[3+index_first_end:]#+1 to be AFTER frac, +1 for first {, +1 for left }
        index_second_end = denominator.find("}")
        denominator = denominator[:index_second_end]
        formula_after = formula_after[3+index_second_end+len(denominator)+2:]# +1 for }, +1 to exclude
        maximum_term = denominator if len(denominator) > len(counter) else counter
        formula = formula_before + maximum_term + formula_after

    # reduce array to longest row:
    if "end{array}" in formula:
        index_start = formula.find(r"\begin{array}")
        formula_before = formula[:index_start-2]#-2 for \\ (because \\ is not found when in .find
        index_end = formula.find(r"\end{array}")
        formula_after = formula[index_end+len(r"\end{array}"):]
        formula_array = formula[index_start+len(r"\begin{array}"):index_end]
        formula_array = formula_array[formula_array.find("}")+1:]# first is the column definition
        # in-between may consist of multiple lines:
        len_part = 0
        for row in formula_array.split(r"\\"):
            # cut out cline:
            if "cline" in row:
                before_cline = row[:row.find(r"\cline")]
                after_cline = row[row.find(r"\cline")+len(r"\cline")+1:]
                after_cline = after_cline[after_cline.find("}")+1:]
                row = before_cline+after_cline
            len_part = max( len_part, get_max_number_of_signs_in_equation(row) )
        return len_part + get_max_number_of_signs_in_equation(formula_before) + get_max_number_of_signs_in_equation(formula_after)
    # determine length of simple equation:
    # print("pure eq:", formula, flush=True)
    formula = formula.replace(r"\\","")
    length = 0
    for s in formula:
        if s.isalpha() or s.isdigit() or s in ["ß","+", "-", "=", ":", " "]:
            length += 1
    return length



def fit_length_to_width(formula:str) -> int:
    number_of_relevant_signs = get_max_number_of_signs_in_equation(eq=formula)
    if "begin{array}" in formula:
        number_of_relevant_signs /= 20
    return math.ceil(42.4 + 14.9 * number_of_relevant_signs)# next higher integer
    # return 5+number_of_relevant_signs



if __name__ == '__main__':
    s = r"\begin{array}{|c|} \hline 1\\ \cline{1-1} 2\\ \cline{1-1} \end{array} \quad \frac{1}{\sqrt{2}} \left( + a_{1} \cdot b_{2}  - a_{2} \cdot b_{1}\right)"

    no = get_max_number_of_signs_in_equation(s)
    w = fit_length_to_width(s)

    print("->", no, w)