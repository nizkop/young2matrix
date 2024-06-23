import copy

from source.function_parts.FunctionDependency import FunctionDependency
from source.function_parts.IntegralPart import IntegralPart
from source.function_parts.TextKinds import TextKinds


class SpinPart(IntegralPart):
    """
    quantum chemical integral representing spin functions
    """
    def __init__(self, permutation_group:int, total_spin:float, ms:float,
                        choices_for_spin:dict, behavior:FunctionDependency):
        self.permutation_group:int=permutation_group
        self.total_spin = total_spin
        self.ms = ms # spin quantum number
        self.function = copy.deepcopy(behavior)
        self.test_choices_for_spin_input(choices_for_spin=choices_for_spin)
        self.choices_for_spin : dict = choices_for_spin
        self.set_up_choices()


    @staticmethod
    def test_choices_for_spin_input(choices_for_spin:dict) -> None:
        """
        testing if the integral function includes the spin functions (alpha, beta), not general functions a, b, c, ...
        :param choices_for_spin: assignment of alpha and beta spins
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
                raise Exception("non-given spin")
        if len(spin_ordered) != self.permutation_group:
            raise Exception("error in set_up_choices")
        self.function.set_spin_functions(spin_ordered)

    def to_text(self) -> str:
        part_1 = f"| {self.get_shortend_form()} >"
        part_2 = f"{self.function.to_text()}"
        return f"{part_1} = {part_2}"

    def to_tex(self) -> str:
        part_1 = r"\ket{ "+fr"{self.total_spin} \quad  {'+' if self.ms >= 0 else '-'}{abs(self.ms)} "+ r"}"
        # part_2 = self.get_normalization_factor()["tex"] + r"\left( "+ self.function.to_tex().replace('α',r"\alpha ").replace('β', r"\beta ")+ r"\right) "
        return fr"{part_1} = {self.function.to_tex()}"

    def get_shortend_form(self, kind:TextKinds=TextKinds.TXT) -> str:
        """ getting the short representation of a spin tableau,
         given by spin total quantum number S and single-particle quantum number ms
        :param kind: choice between using the text as normal text or in latex format
        :return: short version according to | S M_S >
        """
        if kind == TextKinds.TEX:
            return rf" {self.total_spin}\quad {'+' if self.ms >= 0 else '-'}{abs(self.ms)} "
        return f" {self.total_spin}   {'+' if self.ms >= 0 else '-'}{abs(self.ms)} "

