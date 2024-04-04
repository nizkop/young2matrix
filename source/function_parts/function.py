from itertools import permutations
from typing import List

from source.function_parts.product_term import product_term, Sign


class function(object):

    def __init__(self, basis: product_term):
        self.basis = basis
        self.parts: List[product_term] = [basis]

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

    def aggregate_terms(self) -> None:
        """ checking the function term list for duplicates or parts cancelling each other """
        for i in range(len(self.parts)):
            for j in range(i + 1, len(self.parts)):
                if self.parts[i].ordered_functions == self.parts[j].ordered_functions:
                    if self.parts[i].sign.value == self.parts[j].sign.value:
                        self.parts[i].factor += 1
                        del self.parts[j]
                        return self.aggregate_terms()
                    else:
                        del self.parts[j]
                        del self.parts[i]
                        return self.aggregate_terms()



if __name__ == '__main__':
    f = function(product_term(Sign("-"), (1,2,3)))
    f.anti_symmetrize([1,2])
    f.anti_symmetrize([1, 2])
    f.symmetrize([1,3])
    for i in f.parts:
        i.print()
    print("after:")
    f.aggregate_terms()

    for i in f.parts:
        i.print()