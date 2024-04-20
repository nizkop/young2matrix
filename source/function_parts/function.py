import copy
import math
from math import gcd
from fractions import Fraction
from itertools import permutations
from typing import List
import sympy as sp

from source.function_parts.product_term import product_term
from source.function_parts.sign import Sign


class function(object):

    def __init__(self, basis: product_term, normalizable:bool=True):
        self.basis = basis
        self.parts: List[product_term] = [basis]
        self.normalizable:bool=normalizable

    def print(self) -> None:
        print(self.to_text())
    def to_text(self) -> str:
        intern = "  ".join([i.to_text() for i in self.parts])
        return f"{self.get_normalization_factor()['text']} ( {intern} )"

    def to_tex(self) -> str:
        intern = "  ".join([i.to_tex() for i in self.parts])
        return self.get_normalization_factor()["tex"] + r"\left( " + intern.replace('α',r"\alpha ").replace('β', r"\beta ") + r"\right) "

    def get_number_of_terms(self):
        no = 0
        for i in self.parts:
            if i.factor != 0:
                no += i.factor
        return no

    def get_normalization_factor(self) -> dict:
        """
        e.g. (2a + 2b) -> 1/sqrt(2) * (a + b) -> factor = 1/(2*sqrt(2))
        :return:
        """
        if self.get_number_of_terms() == 1 or not self.normalizable:
            return {"text":"", "tex":"", "1/sqrt": 1}
        # n = Fraction(1, math.sqrt(self.get_number_of_terms()**3))
        text = f"1/√({self.get_number_of_terms()}) "
        tex = r"\frac{1}{\sqrt{"+fr"{self.get_number_of_terms()}"+"}} "
        return {"text":text, "tex":tex, "1/sqrt": self.get_number_of_terms()}

    def anti_symmetrize(self, changeble_elements:List[int]):
        return self.permutate_basis(changeable_elements=changeble_elements, change_sign=True)

    def symmetrize(self, changeble_elements:List[int]):
        return self.permutate_basis(changeable_elements=changeble_elements, change_sign=False)

    def permutate_basis(self, changeable_elements:List[int], change_sign:bool) -> None:
        """ helper function for (anti-/)symmetrizing;
        updates the product terms in self.parts according to the switched elements in changeable_elements
        :param change_sign: boolean indicating whether a sign is changeable (anti-symmetric) or not (symmetric)
        """
        new_parts = []
        for part in self.parts:
            p = permutations(changeable_elements)
            # values in part - which are not to be changed - shall be unchanged -> secured at their position
            fixed_elements =[]
            for i in part.ordered_functions:
                if i not in changeable_elements:
                    fixed_elements.append(i)
                else:
                    fixed_elements.append(None)
            # all empty spaces in the list, that are not already determinated, have to be filled by the different permutations:
            for change in p:
                new = fixed_elements[:]
                j = 0
                for i in range(len(new)):
                    if new[i] is None:
                        new[i] = change[j]
                        j+= 1
                if None in new:
                    raise Exception("symmetrize:something went wrong")

                no_of_differences = sum(xi != yi for xi, yi in zip(part.ordered_functions, new))
                sign = Sign(part.sign)
                if change_sign and no_of_differences > 0 and no_of_differences % 2 == 0: # anti-symmetrizing
                    sign = Sign(sign.change())

                new_parts.append(product_term(ordered_functions=tuple(new), sign=sign))
        # renewing with new function parts after the loop:
        self.parts = new_parts


    def reduce_to_least_common_basis(self):
        """ factor out and remove redundant factors in parts
        """
        factors = [i.factor for i in self.parts if i != 0]
        common_div = factors[0]
        for num in factors[1:]:
            common_div = gcd(common_div, num)
        if common_div != 0 and common_div != 1:
            for p in self.parts:
                if p.factor % common_div != 0:
                    raise Exception("wrong rounding / factor finding")
                p.factor //= common_div


    def aggregate_terms(self) -> None:
        """ checking the function term list for duplicates or parts cancelling each other """
        for i in range(len(self.parts)):
            function_list_i = sorted(self.parts[i].get_list_of_parts())
            for j in range(i + 1, len(self.parts)):
                function_list_j = sorted(self.parts[j].get_list_of_parts())
                if self.parts[i].ordered_functions == self.parts[j].ordered_functions or function_list_i == function_list_j:
                    if self.parts[i].sign.value == self.parts[j].sign.value:
                        self.parts[i].factor += 1
                        del self.parts[j]
                        return self.aggregate_terms()
                    else:
                        del self.parts[j]
                        del self.parts[i]
                        return self.aggregate_terms()


    def set_spin_functions(self, spin_functions: List[str]) -> None:
        for i in self.parts:
            i.lowercase_letters = spin_functions
        self.aggregate_terms()
        self.reduce_to_least_common_basis()







if __name__ == '__main__':
    f = function(product_term(Sign("+"), (1,2,3,)))
    f.symmetrize([1,2])
    f.anti_symmetrize([1, 3])
    for i in f.parts:
        i.print()
    # print("after:")
    f.set_spin_functions(["α", "β", "β"])
    # print()
    # for i in f.parts:
    #     i.print()

    f.print()