import copy

from source.function_parts.function import function
from source.function_parts.integral_part import integral_part
from source.function_parts.product_term import product_term
from source.function_parts.sign import Sign
from source.function_parts.text_kinds import text_kinds


class spin_part(integral_part):
    def __init__(self, permutation_group:int, total_spin:float, ms:float, choices_for_spin:dict, behavior:function):
        self.permutation_group:int=permutation_group
        self.total_spin = total_spin
        self.ms = ms
        self.function = copy.deepcopy(behavior)
        self.test_choices_for_spin_input(choices_for_spin=choices_for_spin)
        self.choices_for_spin : dict = choices_for_spin
        self.set_up_choices()


    def test_choices_for_spin_input(self, choices_for_spin) -> None:
        """
        testing if the integral function includes the spin functions (alpha, beta), not general functions a, b, c, ...
        """
        try:
            choices_for_spin["alpha"]
            choices_for_spin["beta"]
        except:
            raise Exception("spin_part-error: choices_for_spin needs input for alpha and beta spins")
        # ms_total = len(choices_for_spin["alpha"]) * 1/2 + len(choices_for_spin["beta"])*(-1/2)
        # if self.ms != ms_total:
        #     raise Exception("spin_part-error: ms does not fit amount of alpha and beta spins")


    def set_up_choices(self) -> None:
        """
        changing the general functions a,b,c,... to spin functions α or β
        """
        spin_ordered = []
        for i in range(1,self.permutation_group+1):
            if i in self.choices_for_spin["alpha"]:
                spin_ordered.append('α')
            elif i in self.choices_for_spin["beta"]:
                spin_ordered.append('β')
            else:
                raise Exception("ungiven spin")
        if len(spin_ordered) != self.permutation_group:
            raise Exception("error in set_up_choices")
        self.function.set_spin_functions(spin_ordered)

    def print(self):
        print(self.to_text())

    def to_text(self):
        part_1 = f"| {self.get_shortend_form()} >"
        part_2 = f"{self.function.to_text()}"
        return f"{part_1} = {part_2}"

    def to_tex(self):
        part_1 = r"\ket{ "+fr"{self.total_spin} \quad  {'+' if self.ms >= 0 else '-'}{abs(self.ms)} "+ r"}"
        # part_2 = self.get_normalization_factor()["tex"] + r"\left( "+ self.function.to_tex().replace('α',r"\alpha ").replace('β', r"\beta ")+ r"\right) "
        return fr"{part_1} = {self.function.to_tex()}"

    def get_shortend_form(self, kind:text_kinds=text_kinds.TXT) -> str:
        """ getting the short representation of a spin tableau, given by spin total quantum number S and single-particle quantum number ms
        :return: short version according to | S M_S >
        """
        if kind == text_kinds.TEX:
            return rf" {self.total_spin}\quad {'+' if self.ms >= 0 else '-'}{abs(self.ms)} "
        return f" {self.total_spin}   {'+' if self.ms >= 0 else '-'}{abs(self.ms)} "

