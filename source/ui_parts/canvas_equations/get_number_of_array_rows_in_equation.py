import copy


def get_number_of_array_rows_in_equation(formula:str):
    formula = copy.deepcopy(formula)
    # print("determine_height_of_equation:", formula, flush=True, end="\t")
    if len(formula.replace(" ","")) == 0:
        return 0
    if not r"\\" in formula or not "begin{array}" in formula:
        return 1
    start = formula.find("begin{array}")
    end = formula.find("end{array}")
    # print(start, end)
    interesting_part = formula[start+len("begin{array}"):end]
    interesting_part = interesting_part.replace(r"\\hline","").replace(r"\\quad","").replace(r"\\cline","").replace(r"\\left[","").replace(r"\\right]","")
    if len(formula[end+len("end{array}"):]) > 0:
        return max(interesting_part.count(r"\\"), get_number_of_array_rows_in_equation(formula[end+len("end{array}"):]))
    return interesting_part.count(r"\\")





