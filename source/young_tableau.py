from typing import List


class young_tableau(object):
    def __init__(self, number_of_rows:int, number_of_columns:List[int]):
        # self.number_of_parts:int=0
        self.number_of_rows:int=number_of_rows
        self.number_of_columns:List[int]=number_of_columns
        self.check()

    def check(self) -> bool:
        """ checking if columns und rows fit to eachother
        :return: boolean indicating if the tableau is set-up correctly """
        if len(self.number_of_columns) != self.number_of_rows:
            # raise Exception("young_tableau: non-fitting dimensions")
            return False
        if not all(self.number_of_columns[i] >= self.number_of_columns[i + 1] for i in range(len(self.number_of_columns) - 1)):
            # raise Exception("young_tableau: unfulfilled young rule")#longer rows at the top
            return False
        return True


    def print(self) -> None:
        if not self.check():
            return
        for i in range(self.number_of_rows):
            for j in range(self.number_of_columns[i]):
                print("[ ]", end=" ")
            print()

    def to_text(self):
        pass

    def get_all_options(self):
        pass

    def get_permutation_group(self) -> int:
        """ calculate the number of boxes in the tableau """
        sum = 0
        for i in range(self.number_of_rows):
            for j in range(self.number_of_columns[i]):
                sum += 1
        return sum



if __name__ == '__main__':
    y = young_tableau(2, [2,1])
    y.print()
    print(y.get_permutation_group())