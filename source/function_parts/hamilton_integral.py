from source.function_combination.calculate_overlap_integral_between_functions import \
    calculate_overlap_integral_between_functions
from source.function_parts.function import function
from source.function_parts.product_term import product_term
from source.function_parts.sign import Sign
from collections import Counter

class hamilton_integral(object):

    def __init__(self, bra:product_term, ket:product_term):
        # print("bra", bra.ordered_functions, bra.lowercase_letters, "ket:", ket.ordered_functions, ket.lowercase_letters)
        # print("calculating... \t <", bra.to_text(), "|H|", ket.to_text(), end=">\t")
        self.factor: int = bra.factor * ket.factor
        self.sign:Sign = Sign.PLUS if bra.sign == ket.sign else Sign.MINUS

        bra.factor = 1
        ket.factor = 1
        bra.sign = Sign.PLUS
        ket.sign = Sign.PLUS
        self.bra:product_term = bra
        self.ket:product_term = ket

        self.check_integral()
        # print("\t\t==\t", self.get_shortened_symbol(), end="\n")

    def __hash__(self):
        return hash(''.join(sorted(self.get_shortened_symbol())))
    def __eq__(self, other):
        return isinstance(other, type(self)) and ''.join(sorted(self.get_shortened_symbol())) == ''.join(sorted(other.get_shortened_symbol()))


    def check_integral(self) -> None:
        """
        multiplying the different functions within the integral and checking, whether there are more than 2 electron switches;
        this function resets the bra and ket attributes
        """
        # print(self.to_text(), end=" ")
        if sorted(self.bra.get_list_of_parts()) == sorted(self.ket.get_list_of_parts()): # identical -> diagonal element
            # print(self.get_shortened_symbol(), self.bra.get_list_of_parts(), self.ket.get_list_of_parts())
            self.bra.lowercase_letters = self.bra.lowercase_letters[:len(self.bra.ordered_functions)]
            self.ket.lowercase_letters = self.ket.lowercase_letters[:len(self.ket.ordered_functions)]
            # print("\ndiagonal",self.factor)
            return

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
                # print("\t\t==\t", self.to_text(), end="\n")
                self.factor = 0
                # print("faktor 0", self.get_shortened_symbol())
                return
        # mehr als 1 Tausch-Paar:
        number_of_pairs = len([x for x in sets.values() if x == 2])
        if number_of_pairs > 1:
             # not more than 1 switching electron pair allowed
            self.factor = 0
            return

        # collecting the non-vanishing parts:
        for k,v in indizes.items():
            # if len(v) == 1: # identical in bra and ket -> ca be multiplied out -> overlaps to 1
            #     f = function(product_term(sign = Sign("+"), ordered_functions=(k, )))
            #     f.parts[0].lowercase_letters = v[0] #not remaining after overlap calculation
            #     o = calculate_overlap_integral_between_functions(f, f)
            #     self.factor *= o.parts[0].factor
            #     # ordered_functions have been reset to [] before
            if len(v) == 2: # switched electrons -> h is effective
                self.bra.ordered_functions.append(k)
                self.ket.ordered_functions.append(k)
                self.bra.lowercase_letters.append(v[0]) # assuming first the bra is read into indizes, THEN the ket
                self.ket.lowercase_letters.append(v[-1]) # ordering because of above assumption
            else: # electron in > 2 orbitals
                pass

        # self.factor *= 2 # only half the matrix is calculated (including the diagonale, thereby this needs to be duplicated, the diagonale not!)

        # print("\t\t==\t", self.get_shortened_symbol(), end="\n")
        # print("normal:", self.get_shortened_symbol())



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
    # p1 = product_term(Sign("-"), (4,3,2,1))
    # p2 = product_term(Sign("-"), (4, 2, 1, 3))
    # h = hamilton_integral(p1, p2)
    # # print(h.to_text())
    #
    # p1 = product_term(Sign("-"), (4,3,2,1))
    # p2 = product_term(Sign("-"), (4, 3,1,2))
    # h = hamilton_integral(p1, p2)
    # print(h.to_text())

    p1 = product_term(Sign("-"), (1,2,4,3))#a1b2d3c4
    p2 = product_term(Sign("+"), (1,3,4,2))#a1d2b3c4
    h = hamilton_integral(p1, p2)
    # print(h.to_text(), h.get_shortened_symbol(), h.factor, h.sign)# < - a_1 * b_2 * c_4 * d_3 |H| + a_1 * b_3 * c_4 * d_2>

