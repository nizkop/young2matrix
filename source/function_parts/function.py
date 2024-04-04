from itertools import permutations
from typing import List

from source.function_parts.product_term import product_term, Sign


class function(object):

    def __init__(self, basis: product_term):
        self.basis = basis
        self.parts: List[product_term] = [basis]


    # def symmetrize(self, index_1:int, index_2:int):
    #     swapped_tuples = self.permutate_basis(index_1=index_1, index_2=index_2)
    #     for swapped_tuple in swapped_tuples:
    #         new = product_term(sign=Sign(self.basis.sign.value), ordered_functions=swapped_tuple)
    #         self.parts.append(new)
    #
    # def permutate_basis(self, original_tuple, index_1:int, index_2:int):
    #     position_in_tuple_1 = original_tuple.ordered_functions.index(index_1)
    #     position_in_tuple_2 = original_tuple.ordered_functions.index(index_2)
    #     swapped_tuple = tuple(index_2 if i == position_in_tuple_1
    #                             else (index_1 if i == position_in_tuple_2
    #                             else original_tuple.ordered_functions[i])
    #                             for i in range(len(original_tuple.ordered_functions)))
    #     return swapped_tuple
    #
    #
    # def anti_symmetrize(self, index_1:int, index_2:int):
    #     swapped_tuple = self.permutate_basis(index_1=index_1, index_2=index_2)
    #     new = product_term(sign=Sign(self.basis.sign.change()), ordered_functions=swapped_tuple)
    #     self.parts.append(new)

    def anti_symmetrize(self, changeble_elements:List[int]):
        return self.permutate_basis(changeable_elements=changeble_elements, change_sign=True)

    def symmetrize(self, changeble_elements:List[int]):
        return self.permutate_basis(changeable_elements=changeble_elements, change_sign=False)

    def permutate_basis(self, changeable_elements:List[int], change_sign:bool) -> None:
        """ helper function for (anti-/)symmetrizing;
        updates the product terms in self.parts according to the switched elements in changeable_elements
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
                    print("changed")

                new_parts.append(product_term(ordered_functions=tuple(new), sign=sign))
        # renewing with new function parts after the loop:
        self.parts = new_parts



if __name__ == '__main__':
    f = function(product_term(Sign("-"), (1,2,3)))
    f.anti_symmetrize([1,2])

    for i in f.parts:
        i.print()