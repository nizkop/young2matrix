
import re


def get_number_of_array_rows_in_equation(formula:str):
    print("determine_height_of_equation:", formula, flush=True, end="\t")
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


def determine_height_of_equation(formula:str) -> int:
    demanded_heights = [70]
    if "array" in formula:
        number_of_rows = get_number_of_array_rows_in_equation(formula)
        print("-> ", number_of_rows)
        height = fit_arrayheight_from_rownumber(number_of_rows)
        demanded_heights.append(height)
    if "frac" in formula:
        height = 95
        if "{\sqrt" in formula:
            height = 100
        demanded_heights.append(height)


    #
    # print("set", height, "for", number_of_rows, flush=True)
    return max(demanded_heights)

def fit_arrayheight_from_rownumber(number_of_rows:int):
    print(f"fit_arrayheight_from_rownumber: 35+35*{number_of_rows} = {35+35*number_of_rows}", flush=True)
    return 35+35*number_of_rows





if __name__ == '__main__':
    testfunctions = [r'\\left[4\\right]:\\quad\\begin{array}{|c|c|c|c|} \\hline 1 & 2 & 3 & 4\\\\ \\cline{1-4} \\end{array} ',
                     r'\\left[13\\right]:\\quad\\begin{array}{|c|c|c|} \\hline 1 & 3 & 4\\\\ \\cline{1-3} 2\\\\ \\cline{1-1} \\end{array} \\quad , \\quad \\begin{array}{|c|c|c|} \\hline 1 & 2 & 4\\\\ \\cline{1-3} 3\\\\ \\cline{1-1} \\end{array} \\quad , \\quad \\begin{array}{|c|c|c|} \\hline 1 & 2 & 3\\\\ \\cline{1-3} 4\\\\ \\cline{1-1} \\end{array} ',
                     r'\\left[2^2\\right]:\\quad\\begin{array}{|c|c|} \\hline 1 & 2\\\\ \\cline{1-2} 3 & 4\\\\ \\cline{1-2} \\end{array} \\quad , \\quad \\begin{array}{|c|c|} \\hline 1 & 3\\\\ \\cline{1-2} 2 & 4\\\\ \\cline{1-2} \\end{array} ',
                     r'\\left[21^2\\right]:\\quad\\begin{array}{|c|c|} \\hline 1 & 4\\\\ \\cline{1-2} 2\\\\ \\cline{1-1} 3\\\\ \\cline{1-1} \\end{array} \\quad , \\quad \\begin{array}{|c|c|} \\hline 1 & 3\\\\ \\cline{1-2} 2\\\\ \\cline{1-1} 4\\\\ \\cline{1-1} \\end{array} \\quad , \\quad \\begin{array}{|c|c|} \\hline 1 & 2\\\\ \\cline{1-2} 3\\\\ \\cline{1-1} 4\\\\ \\cline{1-1} \\end{array} ',
                     r'\\left[1^4\\right]:\\quad\\begin{array}{|c|} \\hline 1\\\\ \\cline{1-1} 2\\\\ \\cline{1-1} 3\\\\ \\cline{1-1} 4\\\\ \\cline{1-1} \\end{array} ']


    for f in testfunctions:
        print(determine_height_of_equation(f))
