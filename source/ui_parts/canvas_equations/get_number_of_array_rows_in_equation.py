import copy


def get_number_of_array_rows_in_equation(formula:str) -> int:
    """
    determine the number of rows in a latex-array-environment within the given formula
    :param formula: latex formatted equation
    :return: number of rows of an array environment
    """
    formula = copy.deepcopy(formula)
    if len(formula.replace(" ","")) == 0:
        return 0
    if not r"\\" in formula or not "begin{array}" in formula:
        return 1
    start = formula.find("begin{array}")
    end = formula.find("end{array}")
    interesting_part = formula[start+len("begin{array}"):end]
    interesting_part = interesting_part.replace(r"\\hline","").replace(r"\\quad","").replace(r"\\cline","").replace(r"\\left[","").replace(r"\\right]","")
    if len(formula[end+len("end{array}"):]) > 0:
        return max(interesting_part.count(r"\\"), get_number_of_array_rows_in_equation(formula[end+len("end{array}"):]))
    return interesting_part.count(r"\\")





