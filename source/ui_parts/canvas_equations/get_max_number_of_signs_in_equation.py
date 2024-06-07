import re
import math

def replace_frac(match: re.Match) -> str:
    """
    replacing a latex-fraction- command by its widest element
    :param match: latex-formatted fraction, found by re search
    :return: needed width of the fraction, given as the longest term within the fraction
    """
    numerator = match.group(1)
    denominator = match.group(2)
    return numerator if len(numerator) > len(denominator) else denominator

def get_max_number_of_signs_in_equation(eq: str) -> int:
    """
    stripping an equation-text of non-displayed characters;
    commands that result in more space after rendering are replaced and the resulting width is accommodated by placeholder characters
    :param eq: latex formatted equation
    :return: width of equation in number of relevant characters
    """
    formula = eq.replace(" ", "")

    # removing unnecessary long LaTeX commands:
    formula = re.sub(r"\\,", "q", formula)
    formula = re.sub(r"\\quad", "qq", formula)
    formula = re.sub(r"\\qquad", "qqq", formula)
    formula = re.sub(r"\\hline|\\cline\{.*?\}|\\underline", "", formula)
    formula = re.sub(r"\\cdot", "**", formula)
    formula = re.sub(r"\\left\(", "(", formula)
    formula = re.sub(r"\\right\)", ")", formula)
    formula = re.sub(r"\\sigma", "S", formula)#"σ"
    formula = re.sub(r"\\alpha", "a", formula)#"α"
    formula = re.sub(r"\\beta", "b", formula)#"β"
    formula = re.sub(r"\\Phi", "P", formula)#"Φ"
    # formula = re.sub(r"\\", "", formula)

    # handling \frac separately:
    while "\\frac" in formula:
        formula = re.sub(r"\\frac\{(.*?)\}\{(.*?)\}", replace_frac, formula)

    # array environments:
    if "\\begin{array}" in formula:
        array_pattern = r"\\begin\{array\}(.*?)\\end\{array\}"
        array_match = re.search(array_pattern, formula, re.DOTALL)
        if array_match:
            array_content = array_match.group(1)
            array_content = array_content[array_content.find("}") + 1:]
            # splitting content into rows -> finding the longest row:
            rows = array_content.split(r"\\")
            max_row_length = max(get_max_number_of_signs_in_equation(row) for row in rows)
            formula = re.sub(array_pattern, "a"*max_row_length, formula, flags=re.DOTALL)
            formula += "padding"

    # simplifying sqrt commands by replacing them with their content:
    formula = re.sub(r"\\sqrt\{(.*?)\}", r"s\1", formula)
    formula = re.sub(r"\\bra\{(.*?)\}\\ket\{(.*?)\}", r"<\1sss\2>", formula)# spacing in the middle (s. tableaus in bra/ket possible)

    # print("remaining:", [formula], len(formula))
    # counting number of relevant characters:
    relevant_characters = re.findall(r"[a-zA-Z0-9ß/ +\-=:&()*\_<>αβσΦ|]", formula)
    return len(relevant_characters)


def fit_length_to_width(formula:str) -> int:
    """
    fit function to translate the width of an equation
     given as the number of relevant signs into a pixel size
    :param formula: latex formatted equation
    :return: needed width of equation in pixels
    """
    number_of_relevant_signs = get_max_number_of_signs_in_equation(eq=formula)
    # print("number_of_relevant_signs", number_of_relevant_signs)
    return max(number_of_relevant_signs, math.ceil(29.04 + 15.10 * number_of_relevant_signs))# next higher integer

