from source.function_combination.calculate_overlap_integral_between_functions import \
    calculate_overlap_integral_between_functions
from source.function_parts.function import function
from source.function_parts.product_term import product_term
from source.function_parts.sign import Sign
from collections import Counter

class hamilton_integral(object):

    def __init__(self, bra:product_term, ket:product_term):
        # print("bra", bra.ordered_functions, bra.lowercase_letters, "ket:", ket.ordered_functions, ket.lowercase_letters)
        self.factor: int = bra.factor * ket.factor
        self.sign :Sign = Sign.PLUS if bra.sign == ket.sign else Sign.MINUS

        bra.factor = 1
        ket.factor = 1
        bra.sign = Sign.PLUS
        ket.sign = Sign.PLUS
        self.bra:product_term = bra
        self.ket:product_term = ket

        self.check_integral()

    def __hash__(self):
        return hash(self.get_shortened_symbol())
    def __eq__(self, other):
        return isinstance(other, type(self)) and ''.join(sorted(self.get_shortened_symbol())) == ''.join(sorted(other.get_shortened_symbol()))


    def check_integral(self) -> None:
        """
        multiplying the different functions within the integral and checking, whether there are more than 2 electron switches;
        this function resets the bra and ket attributes
        """
        indizes = self.get_occurence_of_indizes()
        self.bra.ordered_functions = []
        self.bra.lowercase_letters = []
        self.ket.ordered_functions = []
        self.ket.lowercase_letters = []

        # checking if uneven number of switched functions:
        sets = {}
        for v in indizes.values():
            key = str("".join(sorted(v)))
            try:
                sets[key] += 1
            except KeyError:
                sets[key] = 1
        for set_key, set_value in sets.items():
            if len(set_key) == 2 and set_value != 2: # always a pair needed
                return

        for k,v in indizes.items():
            if len(v) == 1: # identical in bra and ket -> ca be multiplied out -> overlaps to 1
                f = function(product_term(sign = Sign("+"), ordered_functions=(k, )))
                f.parts[0].lowercase_letters = v[0] #not remaining after overlap calculation
                o = calculate_overlap_integral_between_functions(function, function)
                self.factor *= o.parts[0].factor
                # ordered_functions have been reset to [] before
            elif len(v) == 2: # switched electrons -> h is effective
                self.bra.ordered_functions.append(k)
                self.ket.ordered_functions.append(k)
                self.bra.lowercase_letters.append(v[0]) # assuming first the bra is read into indizes, THEN the ket
                self.ket.lowercase_letters.append(v[-1]) # ordering because of above assumption
            else: # electron in > 2 orbitals!?
                pass



    def get_occurence_of_functions(self):
        #count occurences of functions in bra and ket
        functions = {}
        lists = [self.bra, self.ket]
        for list in lists:
            for i in range(len(list.ordered_functions)):
                if list.lowercase_letters[i] in functions.keys():
                    if list.ordered_functions[i] not in functions[list.lowercase_letters[i]]:
                        functions[list.lowercase_letters[i]].append(list.ordered_functions[i] )
                else:
                    functions[list.lowercase_letters[i]] = [list.ordered_functions[i]]
        return functions

    def get_occurence_of_indizes(self) -> dict:
        indizes = {}
        lists = [self.bra, self.ket]
        for list in lists:
            for i in range(len(list.ordered_functions)):
                if list.ordered_functions[i] in indizes.keys():
                    if list.lowercase_letters[i] not in indizes[list.ordered_functions[i]]:
                        indizes[list.ordered_functions[i]].append(list.lowercase_letters[i] )
                else:
                    indizes[list.ordered_functions[i]] = [list.lowercase_letters[i]]
        return indizes


    def to_text(self) -> str:
        if self.bra.factor == 1 and self.ket.factor == 1 and len(self.bra.ordered_functions) == 0 and len(self.ket.ordered_functions) == 0:
            return f" {self.sign.value} {self.factor}"  # integral reverted to overlap (which is only a number, not an integral anymore)
        return f" {self.sign.value} {self.factor} * <{self.bra.to_text().replace('+','')} |H| {self.ket.to_text().replace('+','')} >".replace(' '*2,' ')


    def get_shortened_symbol(self) -> str:
        return "".join(set(self.bra.lowercase_letters+self.ket.lowercase_letters))


#
if __name__ == '__main__':
    p1 = product_term("+", (4,3,2,1))
    p2 = product_term("+", (4, 2, 1, 3))
    hamilton_integral(p1, p2)

    p1 = product_term("+", (4,3,2,1))
    p2 = product_term("+", (4, 3,1,2))
    hamilton_integral(p1, p2)