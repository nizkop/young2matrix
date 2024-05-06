from typing import List, Dict


class young_tableau(object):
    def __init__(self, number_of_rows:int, number_of_columns:List[int]):
        # self.number_of_parts:int=0
        self.number_of_rows:int=number_of_rows
        self.numbers_in_columns:List[int]=number_of_columns
        self.check()


    def check(self) -> bool:
        """ checking if columns und rows fit to eachother
        :return: boolean indicating if the tableau is set-up correctly """
        if len(self.numbers_in_columns) != self.number_of_rows:
            # raise Exception("young_tableau: non-fitting dimensions")
            return False
        if not all(self.numbers_in_columns[i] >= self.numbers_in_columns[i + 1] for i in range(len(self.numbers_in_columns) - 1)):
            # raise Exception("young_tableau: unfulfilled young rule")#longer rows at the top
            return False
        return True


    def print(self) -> None:
        if not self.check():
            return
        print(self.get_shortend_symbol()["plain_text"])
        print(self.to_text())

    def to_text(self) -> str:
        s=""
        for i in range(self.number_of_rows):
            for j in range(self.numbers_in_columns[i]):
                s+="[ ] "
            s+="\n"
        return s

    def get_permutation_group(self) -> int:
        """ calculate the number of boxes in the tableau """
        sum = 0
        for i in range(self.number_of_rows):
            for j in range(self.numbers_in_columns[i]):
                sum += 1
        return sum

    def get_shortend_symbol(self) -> Dict[str, str]:
        parts = "".join([str(i) for i in self.numbers_in_columns]) # getting the relevant numbers
        parts = ''.join([f"{char}^{parts.count(char)}" if parts.count(char) > 1 else char for char in set(parts)])#replace multiples with power
        return {"plain_text": f"[{parts}]", "tex": rf"\left[{parts}\right]"}




if __name__ == '__main__':
    y = young_tableau(2, [2,2,1,1])
    y.print()
    # print(y.get_permutation_group())
    print(y.get_shortend_symbol())