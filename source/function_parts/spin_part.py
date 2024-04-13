from source.function_parts.integral_part import integral_part


class spin_part(integral_part):
    def __init__(self, total_spin:float, ms:float):
        self.permutation_group:int=0
        self.behavior = None
        self.choices_for_spin : dict = {}
        self.total_spin = total_spin
        self.ms = ms

    def print(self):
        print(self.to_text())

    def to_text(self):
        return f"| {self.total_spin}  {'+' if self.ms >= 0 else '-'}{abs(self.ms)} >"

    def to_tex(self):
        return "\ket{ "+fr"{self.total_spin} \quad  {'+' if self.ms >= 0 else '-'}{abs(self.ms)} "+ "}"

    # def find_all_choices(self):
    #     pass

    def get_spin_part(self):#TODO
        pass