from source.ui_parts.canvas_equations.get_number_of_array_rows_in_equation import get_number_of_array_rows_in_equation


def determine_height_of_equation(formula: str) -> int:
    """
    determining the height of an equation
    by its properties like included fractions or other items that need more vertical space
    :param formula: latex equation to-be displayed
    :return: maximal height
    """
    demanded_heights = [70]#<- default = minimal height of equation
    if "array" in formula:
        number_of_rows = get_number_of_array_rows_in_equation(formula)
        height = fit_arrayheight_from_rownumber(number_of_rows)
        demanded_heights.append(height)
    if "frac" in formula:
        height = 95
        if "{\sqrt" in formula:
            height = 100
        demanded_heights.append(height)
    return max(demanded_heights)


def fit_arrayheight_from_rownumber(number_of_rows: int) -> int:
    """ fit function to translate the number of rows in an equation into the amount of needed pixels
    :param number_of_rows: height of equation in number of rows
    :return: needed height in pixels
    """
    return 35 + 35 * number_of_rows

