from source.function_parts.function import function
from source.function_parts.integral_part import integral_part


class spatial_part(integral_part):
    """
    class only needed for coherence, because spatial functions are the opposite of spin functions
    but spatial functions/orbitals are not specifically given here, so that spatial parts fall back to the general integral parts
    """
    def __init__(self,behavior:function):
        self.permutation_group : int = 0
        self.function = behavior
        self.choices_for_quantum_number_ml : dict = {}

    # def print(self):
    #     pass
    #
    # def to_tex(self) -> str:
    #     return self.function.to_tex()
    #
    # def to_text(self) -> str:
    #     return self.function.to_text()
    #
    # def find_all_choices(self):
    #     pass
    #
    # def get_spatial_part(self):
    #     pass