
from collections import Counter
import string
from fractions import Fraction
from typing import Tuple, List

from source.function_parts.Sign import Sign



class ProductTerm(object):
    """
    general integral product including multiple functional terms
    """
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
        """ combine functions into a list: functions a,b,c are paired with their indices 1,2,3,...
        items in the lists are factors and need to be multiplicated with each other later on
        :return: list of functions (as factors of eachother)
        """
        counter = Counter(zip(self.lowercase_letters, self.ordered_functions))
        return [str(key[0]) + r"_{"+str(key[1])+r"}^{"+str(count)+"}"
                if count > 1
                else str(key[0]) + r"_{"+str(key[1])+r"}"
                for key, count in counter.items()]

    def to_text(self) -> str:
        return self.to_tex().replace("{","").replace("}","").replace(r"\cdot","*")
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
        if self.factor == 1:
            factor = ""
        elif isinstance(self.factor, Fraction):
            factor = r"\frac{"+ str(self.factor.numerator) + r"}{" + str(self.factor.denominator) + r"} \cdot "
        else:
            factor = fr"{self.factor} \cdot "
        function_factors = r" \cdot ".join(self.get_list_of_parts())
        eq = sign+factor+function_factors
        return eq.replace("α",r"\alpha").replace("β",r"\beta")

    def multiply(self, other#: product_term
        ):# -> product_term
        """ building a product of products = simple factor combination (for numbers and functions)
        grouping happens later on, here duplicates of functions x_i may occur
        :param other: other product term, being multiplied with this object
        :return: new product_term object, that is the product of the given terms
        """
        new_factor = self.factor * other.factor
        new_sign = Sign("+") if self.sign.value == other.sign.value else Sign("-")

        p = ProductTerm(new_sign, other.ordered_functions)
        p.factor = new_factor
        p.lowercase_letters = p.lowercase_letters[:len(p.ordered_functions)] * 2
        p.ordered_functions = tuple( list(p.ordered_functions) + list(self.ordered_functions) )
        return p

    def integrational_multiply(self, other#: product_term
        ) -> Tuple:
        """
        building a bra and ket equation form two product_term objects;
        orthonormed functions: <a|b> = <a|c> = ... = 0
        :param other: other product term, building the ket
        :return: integral information (overlap) = what was combined (1.) and the result (2.)
        """
        eq_left = f"< {self.to_text()} | {other.to_text()} >"
        empty_part = ProductTerm(Sign.PLUS if self.sign == other.sign else Sign.MINUS, ())
        if sorted(self.get_list_of_parts()) != sorted(other.get_list_of_parts()):
            empty_part.factor = 0
        else:
            empty_part.factor = abs( self.factor * other.factor * 1 )
        return empty_part, eq_left

