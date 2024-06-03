from typing import List, Union, Tuple

from source.function_parts.function import function
from source.function_parts.product_term import product_term
from source.function_parts.sign import Sign
from source.young_tableau import young_tableau


class standard_tableau(young_tableau):

    def __init__(self, numbers_in_row:List[Tuple[int,...]]):
        super().__init__(number_of_rows=len(numbers_in_row), number_of_columns=[len(i) for i in numbers_in_row])
        self.numbers_in_row:List[tuple[int,...]] = numbers_in_row
        self.permutation_group: int = self.get_permutation_group()
        self.function: Union[function, None] = None

    def print(self) -> None:
        print(self.to_text())

    def check(self) -> bool:
        """ checking the rules of standard tableau (numbers ascending in rows and columns)
         :return: boolean indicating whether this tableau is a standard tableau
         """
        if not super().check():
            return False
        if not hasattr(self, 'numbers_in_row'):
            return False # not initialized yet
        all_numbers = [element for sublist in self.numbers_in_row for element in sublist]
        if len(set(all_numbers)) != len(all_numbers):
            # raise Exception("standard_tableau: no duplicate numbers allowed")
            return False
        for row in self.numbers_in_row:
            if not all(row[i] <= row[i + 1] for i in range(len(row) - 1)):
                # raise Exception("standard_tableau: numbers have to be ascending in a row")
                return False
        for column in self.get_numbers_in_columns():
            if not all(column[i] <= column[i+1] for i in range(len(column)-1)):
                # raise Exception("standard_tableau: numbers have to be ascending in a column")
                return False
        return True

    def get_numbers_in_columns(self) -> List[List[int]]:
        """ reverting the list of numbers in a row into a list of numbers in a column
        :return: list of numbers per column
        """
        max_length = max(len(row) for row in self.numbers_in_row)
        spalten = []
        for i in range(max_length):
            column = []
            for row in self.numbers_in_row:
                 if i < len(row):
                     column.append(row[i])
            spalten.append(column)
        return spalten
        #  return [[row[i] for row in self.numbers_in_row if i < len(row)] for i in range(max_length)]

    def get_number_of_columns(self):
        return max([len(x) for x in self.numbers_in_row])


    def to_text(self) -> str:
        s = ""
        if self.check():
            for i in range(self.number_of_rows):
                for j in range(self.numbers_in_columns[i]):
                    s+= f"[{self.numbers_in_row[i][j]}] "
                s+= "\n"
        return s

    def to_tex(self) -> str:
        s = r""
        if self.check():
            s = r"\begin{array}{" + r"|c" * max(self.numbers_in_columns) + r"|} \hline "
            for i in range(self.number_of_rows):
                s+= r" & ".join([f"{self.numbers_in_row[i][j]}" for j in range(self.numbers_in_columns[i])])
                s+= r"\\ \cline{1"
                s+= rf"-{len(self.numbers_in_row[i])}"
                s+= r"} "
        return s+r"\end{array} "

    def get_permutation_group(self) -> int:
        """ calculate the number of boxes in the tableau
        :return sum: number of permutation group
        """
        sum = 0
        for i in range(self.number_of_rows):
            for j in range(self.numbers_in_columns[i]):
                sum += 1
        return sum

    def set_up_function(self) -> None:
        """ initialize function, apply young operator to tableau and multiply out the different terms
        :return None: because result is written into self.function
        """
        if not self.check():
            return
        if self.function is not None:
            return
        self.function = function(product_term( Sign("+"), tuple(i+1 for i in range(self.permutation_group))  ))
        # use young operator:
        for row in self.numbers_in_row:
            self.function.symmetrize(list(row))
        for column in self.get_numbers_in_columns():
            self.function.anti_symmetrize(column)
        self.function.aggregate_terms()
        self.function.reduce_to_least_common_basis()

