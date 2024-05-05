
from collections import Counter
import string
from typing import Tuple, List

from source.function_parts.sign import Sign



class product_term(object):
    def __init__(self, sign: Sign, ordered_functions:Tuple[int,...]):
        self.sign: Sign = sign
        self.factor:int = 1
        self.ordered_functions = ordered_functions # always in order a, b, c, ...; indices variate
        self.lowercase_letters = list(string.ascii_lowercase)
        # ensuring enough available function names in lowercase_letters:
        x = 2
        while len(self.lowercase_letters) < len(self.ordered_functions):
            self.lowercase_letters += [ x*i for i in self.lowercase_letters ]
            x+=1

    def get_list_of_parts(self) -> List[str]:
        counter = Counter(zip(self.lowercase_letters, self.ordered_functions))
        return [str(key[0]) + r"_{"+str(key[1])+r"}^{"+str(count)+"}"
                if count > 1
                else str(key[0]) + r"_{"+str(key[1])+r"}"
                for key, count in counter.items()]

    def to_text(self) -> str:
        return self.to_tex().replace("{","").replace("}","").replace(r"\cdot","*")

    def print(self) -> None:
        print(self.to_text())

    def to_tex(self) -> str:
        sign = f"{self.sign.value} "
        if len(self.ordered_functions) == 0:
            if self.factor == 0:
                return "0"
            else:
                return sign+str(self.factor)
        if len(self.ordered_functions) == 0:
            if self.factor == 0:
                return "0"
            else:
                return sign+str(self.factor)
        factor = fr"{self.factor} \cdot " if self.factor > 1 else ""
        function_factors = r" \cdot ".join(self.get_list_of_parts())
        eq = sign+factor+function_factors
        return eq.replace("α",r"\alpha").replace("β",r"\beta")


    def multiply(self, other):# -> product_term
        """ building a product of products = simple factor combination (for numbers and functions)
        grouping happens later on, here duplicates of functions x_i may occur
        """
        new_factor = self.factor * other.factor
        new_sign = Sign("+") if self.sign.value == other.sign.value else Sign("-")

        p = product_term(new_sign, other.ordered_functions)
        p.factor = new_factor
        p.lowercase_letters = p.lowercase_letters[:len(p.ordered_functions)] * 2
        p.ordered_functions = tuple( list(p.ordered_functions) + list(self.ordered_functions) )

        #print(f"{self.to_text()}       *       {other.to_text()}     =     {p.to_text()}")
        return p

    def integrational_multiply(self, other):
        """
        orthonormed functions: <a|b> = <a|c> = ... = 0
        :param other:
        :return:
        """
        eq_left = f"< {self.to_text()} | {other.to_text()} >"
        empty_part = product_term(Sign.PLUS if self.sign == other.sign else Sign.MINUS, ())
        if sorted(self.get_list_of_parts()) != sorted(other.get_list_of_parts()):
            empty_part.factor = 0
        else:
            empty_part.factor = abs( self.factor * other.factor * 1 )
        # eq_right = empty_part.to_text()
        # print(eq_left , "=", empty_part.to_text())
        return empty_part, eq_left





if __name__ == '__main__':
    p = product_term(Sign("+"), (2,1))
    p.factor = 2
    p.lowercase_letters = ["α", "β"]*3
    # p.print()
    # print(p.to_tex())
    q = product_term(Sign("+"), ordered_functions=(1,2))

    p.integrational_multiply(q)

    # p=product_term(Sign("+"), (1,2,))
    # p.lowercase_letters = p.lowercase_letters[:len(p.ordered_functions)] * 2
    # p.ordered_functions = (1,2,2,1)
    # p.print()




