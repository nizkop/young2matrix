

import string
from enum import Enum

class Sign(Enum):
    PLUS = '+'
    MINUS = '-'



class product_term(object):
    def __init__(self, sign:Sign, ordered_functions:tuple[int]):
        self.sign:Sign = sign
        self.ordered_functions = ordered_functions # always in order a, b, c, ...; indizes variating
        self.lowercase_letters = list(string.ascii_lowercase)
        # ensuring enough available function names in lowercase_letters:
        x = 2
        while len(self.lowercase_letters) < len(self.ordered_functions):
            self.lowercase_letters += [ x*i for i in self.lowercase_letters ]
            x+=1

    def to_text(self) -> str:
        s = f"{self.sign.value} "
        s+=" * ".join([ f"{self.lowercase_letters[i]}{self.ordered_functions[i]}" for i in range(len(self.ordered_functions))])
        return s

    def print(self) -> None:
        print(self.to_text())

    def to_tex(self) -> str:
        s = fr"{self.sign.value} "
        s+=r" \cdot ".join([ fr"{self.lowercase_letters[i]}_{self.ordered_functions[i]}" for i in range(len(self.ordered_functions))])
        return s



if __name__ == '__main__':
    p = product_term(Sign("-"), (1,2,3,4,5,6))
    p.print()
    print(p.to_tex())