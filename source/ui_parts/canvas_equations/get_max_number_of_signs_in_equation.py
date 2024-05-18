import copy
import math

#
# def get_max_number_of_signs_in_equation(eq:str) -> int:
#     formula = copy.deepcopy(eq)
#     # print("get_max_number_of_signs_in_equation", formula)
#
#     formula = formula.replace(" ", "")# is displayed in UI!
#     formula = formula.replace(r"\\hline","").replace(r"\hline","")
#     formula = formula.replace(r"\\quad","pp").replace(r"\\qquad","ppp")#placeholders
#     formula = formula.replace(r"\quad", "pp").replace(r"\qquad", "ppp")  # placeholders
#     formula = formula.replace(r"\\cdot", "m").replace(r"\cdot","m")
#     if len(formula) == 0:
#         return 0
#     # reduce frac to longest part:
#     while "frac" in formula:
#         index = formula.find(r"\frac")
#         formula_before = formula[:index]
#         formula_after = formula[index+len(r"\frac")+1:]
#         counter = formula[index+len(r"\frac")+1:]
#         index_first_end = counter.find("}")
#         counter = counter[:index_first_end] #.replace("{","").replace("}","")
#         denominator = formula_after[3+index_first_end:]#+1 to be AFTER frac, +1 for first {, +1 for left }
#         index_second_end = denominator.find("}")
#         denominator = denominator[:index_second_end]
#         formula_after = formula_after[3+index_second_end+len(denominator)+2:]# +1 for }, +1 to exclude
#         maximum_term = denominator if len(denominator) > len(counter) else counter
#         formula = formula_before + maximum_term + formula_after
#
#     # reduce array to longest row:
#     if "end{array}" in formula:
#         index_start = formula.find(r"\begin{array}")
#         formula_before = formula[:index_start-2]#-2 for \\ (because \\ is not found when in .find
#         index_end = formula.find(r"\end{array}")
#         formula_after = formula[index_end+len(r"\end{array}"):]
#         formula_array = formula[index_start+len(r"\begin{array}"):index_end]
#         formula_array = formula_array[formula_array.find("}")+1:]# first is the column definition
#         # in-between may consist of multiple lines:
#         len_part = 0
#         for row in formula_array.split(r"\\"):
#             # cut out cline:
#             if "cline" in row:
#                 row = shorten_command_to_content(s=row, command="\cline", remove_completely=True)
#                 # before_cline = row[:row.find(r"\cline")]
#                 # after_cline = row[row.find(r"\cline")+len(r"\cline")+1:]
#                 # after_cline = after_cline[after_cline.find("}")+1:]
#                 # row = before_cline+after_cline
#             len_part = max( len_part, get_max_number_of_signs_in_equation(row) )
#             # print("row:", row, len(row))
#         # print("len_part", len_part, get_max_number_of_signs_in_equation(formula_before) , get_max_number_of_signs_in_equation(formula_after))
#         return len_part + get_max_number_of_signs_in_equation(formula_before) + get_max_number_of_signs_in_equation(formula_after)
#     # determine length of simple equation:
#     # print("pure eq:", formula, flush=True)
#     formula = shorten_command_to_content(s=formula, command=r"\sqrt", remove_completely=False)
#     formula = formula.replace(r"\\","")
#     length = 0
#     for s in formula:
#         if s.isalpha() or s.isdigit() or s in ["ß","+", "-", "=", ":", " "]:
#             print(s, end="")
#             length += 1
#     print()
#     return length
#
#
# def shorten_command_to_content(s:str, command:str, remove_completely:bool=False):
#     before_c = s[:s.find(command)]
#     inbetween_c = s[s.find(command) + len(command) + 1:]
#     after_c = inbetween_c[inbetween_c.find("}") + 1:]
#     inbetween_c = inbetween_c[:inbetween_c.find("}")]
#     if remove_completely:
#         return before_c + after_c
#     return before_c+inbetween_c+after_c
#
#
#
from tst import get_max_number_of_signs_in_equation


def fit_length_to_width(formula:str) -> int:
    number_of_relevant_signs = get_max_number_of_signs_in_equation(eq=formula)
    print("number_of_relevant_signs", number_of_relevant_signs)
    # if "begin{array}" in formula:
    #     number_of_relevant_signs /= 20
    return max(number_of_relevant_signs, math.ceil(29.04 + 15.10 * number_of_relevant_signs))# next higher integer
    # return 5+number_of_relevant_signs
#
#
#
# if __name__ == '__main__':
#
#     # print(shorten_command_to_content(s="\sqrt{2}", command=r"\sqrt"))
#     s = r"\begin{array}{|c|} \hline 1\\ \cline{1-1} 2\\ \cline{1-1} \end{array} \quad \frac{1}{\sqrt{2}} \left( + a_{1} \cdot b_{2}  - a_{2} \cdot b_{1}\right)"
#
#     no = get_max_number_of_signs_in_equation(s)
#     w = fit_length_to_width(s)
#
#     print("->", no, w)