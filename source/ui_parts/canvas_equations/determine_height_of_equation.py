from source.ui_parts.canvas_equations.get_number_of_array_rows_in_equation import get_number_of_array_rows_in_equation


def determine_height_of_equation(formula: str) -> int:
    demanded_heights = [70]#<- default = minimal height of equation
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

    return max(demanded_heights)


def fit_arrayheight_from_rownumber(number_of_rows: int):
    # print(f"fit_arrayheight_from_rownumber: 35+35*{number_of_rows} = {35 + 35 * number_of_rows}", flush=True)
    return 35 + 35 * number_of_rows

