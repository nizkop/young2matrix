
from fractions import Fraction
import sympy as sp

from source.function_parts.function import function
from source.function_parts.product_term import product_term
from source.function_parts.sign import Sign
from source.standard_tableau import standard_tableau


class function_combination(object):
    def __init__(self, tableau_a: standard_tableau, tableau_b:standard_tableau):
        self.tableau_a : standard_tableau = tableau_a
        self.tableau_b : standard_tableau = tableau_b

    def calculate_overlap_integral(self) -> function:
        # TODO: not correct yet
        if self.tableau_a.permutation_group != self.tableau_b.permutation_group:
            raise Exception("function_combination error: The tableaus dont fit.")
        empty_function = function(product_term(Sign("+"), ()),normalizable=False)
        # check if identical form
        if self.tableau_a.number_of_rows != self.tableau_b.number_of_rows or self.tableau_a.number_of_columns != self.tableau_b.number_of_columns:
            # basis function of young tableaux from different young diagrams are automatically diagonal
            empty_function.parts[0].factor = 0
            empty_function.parts = [empty_function.parts[0]]
        # same young diagram (form):

        # test if same standard tableau:
        elif self.tableau_a.numbers_in_row == self.tableau_b.numbers_in_row:
            empty_function.parts[0].factor = 1
            empty_function.parts[0].ordered_functions = ()
            empty_function.parts = [empty_function.parts[0]]

        else:
            factor_of_non_cancelled_terms = 0
            norm = self.tableau_a.function.get_normalization_factor()["1/sqrt"] * self.tableau_b.function.get_normalization_factor()["1/sqrt"]
            total_eq = ""
            left_eq = ""
            no_of_terms = 0
            for i in self.tableau_a.function.parts:
                for j in self.tableau_b.function.parts:
                    no_of_terms += 1
                    p, eq_braket = i.integrational_multiply(j)
                    total_eq +=" + "+ eq_braket
                    if p.factor != 0:
                        left_eq += p.to_text()
                    if p.sign == Sign.PLUS:
                        factor_of_non_cancelled_terms += p.factor
                    else:
                        factor_of_non_cancelled_terms -= p.factor
                    if p.factor != 0:
                        empty_function.parts.append(p)
            # empty_function.parts[0].factor = Fraction(factor_of_non_cancelled_terms, sp.sqrt(norm))
            print(total_eq, "\n\n= ", left_eq, "\nnumber of terms:", no_of_terms, "\n")
        empty_function.print()
        return empty_function





    def calculate_hamilton_integral(self):
        pass




if __name__ == '__main__':
    s = standard_tableau([(1, 2, ), (3, 4,)])
    s.set_up_function()
    s.function.print()
    print("\n")

    t = standard_tableau([(1, 3,), (2, 4,)])
    t.set_up_function()

    f = function_combination(s, t)
    f.calculate_overlap_integral()
