import copy

from source.function_parts.function import function
from source.function_parts.integral_part import integral_part


class spin_part(integral_part):
    def __init__(self, permutation_group:int, total_spin:float, ms:float, choices_for_spin:dict, behavior:function):
        self.permutation_group:int=permutation_group
        self.behavior = None
        self.total_spin = total_spin
        self.ms = ms
        self.function = copy.deepcopy(behavior)
        self.test_choices_for_spin_input(choices_for_spin=choices_for_spin)
        self.choices_for_spin : dict = choices_for_spin
        self.set_up_choices()

    def test_choices_for_spin_input(self, choices_for_spin):
        try:
            choices_for_spin["alpha"]
            choices_for_spin["beta"]
        except:
            raise Exception("spin_part-error: choices_for_spin needs input for alpha and beta spins")
        # ms_total = len(choices_for_spin["alpha"]) * 1/2 + len(choices_for_spin["beta"])*(-1/2)
        # if self.ms != ms_total:
        #     raise Exception("spin_part-error: ms does not fit amount of alpha and beta spins")


    def set_up_choices(self):
        # "α", "β"
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
        for p in self.function.parts:
            p.lowercase_letters = spin_ordered
        self.function.aggregate_terms()

    def print(self):
        print(self.to_text())

    def to_text(self):
        part_1 = f"| {self.total_spin}  {'+' if self.ms >= 0 else '-'}{abs(self.ms)} >"
        part_2 = self.function.to_text()
        return f"{part_1} = {part_2}"

    def to_tex(self):
        part_1 = r"\ket{ "+fr"{self.total_spin} \quad  {'+' if self.ms >= 0 else '-'}{abs(self.ms)} "+ r"}"
        part_2 = self.function.to_tex().replace('α',r"\alpha ").replace('β', r"\beta ")
        return fr"{part_1} = {part_2}"

    # def find_all_choices(self):
    #     pass

    def get_spin_part(self):#TODO
        pass


if __name__ == '__main__':
    s = spin_part(2,2,{"alpha":[1,2,3,4], "beta":[]})