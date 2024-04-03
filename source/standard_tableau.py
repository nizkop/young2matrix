from typing import List

from source.young_tableau import young_tableau


class standard_tableau(young_tableau):

    def __init__(self, numbers_in_row:List[tuple[int]]):
        super().__init__(number_of_rows=len(numbers_in_row), number_of_columns=[len(i) for i in numbers_in_row])
        self.numbers_in_row:List[tuple[int]] = numbers_in_row
        self.permutation_group: int = self.get_permutation_group()

    def print(self) -> None:
        if self.check():
            for i in range(self.number_of_rows):
                for j in range(self.number_of_columns[i]):
                    print(f"[{self.numbers_in_row[i][j]}]", end=" ")
                print()

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
        """ reverting the list of numbers in a row into a list of numbers in a column """
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


    def to_text(self):
        pass

    def get_permutation_group(self) -> int:
        """ calculate the number of boxes in the tableau """
        sum = 0
        for i in range(self.number_of_rows):
            for j in range(self.number_of_columns[i]):
                sum += 1
        return sum


if __name__ == '__main__':
    s = standard_tableau([[1,2],[3]])
    s.print()

    print(s.get_permutation_group())