from typing import List, Dict


class YoungTableau(object):
    """
    young tableau:
    = mathematical object used in combinatorics or group theory
    = finite collection of boxes arranged in rows and columns s.t.
        - number of boxes in a row is decreasing with row number (top to bottom)
        - number of boxes in a column is descresing with column number (left to right)
    """
    def __init__(self, number_of_rows:int, number_of_columns:List[int]):
        self.number_of_rows:int=number_of_rows
        self.numbers_in_columns:List[int]=number_of_columns
        self.check()


    def check(self) -> bool:
        """ checking if columns und rows fit to eachother
        :return: boolean indicating whether the tableau is set up correctly """
        if len(self.numbers_in_columns) != self.number_of_rows:
            # raise Exception("young_tableau: non-fitting dimensions")
            return False
        if not all(self.numbers_in_columns[i] >= self.numbers_in_columns[i + 1] for i in range(len(self.numbers_in_columns) - 1)):
            # raise Exception("young_tableau: unfulfilled young rule")#longer rows at the top
            return False
        return True

    def to_text(self) -> str:
        s=""
        for i in range(self.number_of_rows):
            for j in range(self.numbers_in_columns[i]):
                s+="[ ] "
            s+="\n"
        return s

    def get_permutation_group(self) -> int:
        """ calculate the number of boxes in the tableau
        :return: number of elements in the group
        """
        sum_elements = 0
        for i in range(self.number_of_rows):
            for j in range(self.numbers_in_columns[i]):
                sum_elements += 1
        return sum_elements

    def get_shortened_symbol(self) -> Dict[str, str]:
        """
        short version of representing a young tableau by listing the number of boxes in a row
        (combining identical values by setting an exponent)
        :return: shortened information, split into the different visualization choices (text/latex)
        """
        parts = "".join([str(i) for i in self.numbers_in_columns]) # getting the relevant numbers
        parts = ''.join([f"{char}^{parts.count(char)}" if parts.count(char) > 1 else char for char in set(parts)])#replace multiples with power
        return {"plain_text": f"[{parts}]", "tex": rf"\left[{parts}\right]"}


