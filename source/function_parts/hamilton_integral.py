from source.function_parts.product_term import product_term
from source.function_parts.sign import Sign


class hamilton_integral(object):

    def __init__(self, bra:product_term, ket:product_term):
        self.factor: int = bra.factor * ket.factor
        self.sign :Sign = Sign.PLUS if bra.sign == ket.sign else Sign.MINUS

        bra.factor = 1
        ket.factor = 1
        bra.sign = Sign.PLUS
        ket.sign = Sign.PLUS
        self.bra:product_term = bra
        self.ket:product_term = ket

        self.check_integral()


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

        for k,v in indizes.items():
            if len(v) == 1: # identical in bra and ket -> ca be multiplied out -> overlaps to 1
                pass
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
        return f" {self.sign.value} {self.factor} * <{self.bra.to_text().replace('+','')} |H| {self.ket.to_text().replace('+','')} >".replace(' '*2,' ')


    def get_shortened_symbol(self) -> str:
        return "".join(set(self.bra.lowercase_letters+self.ket.lowercase_letters))