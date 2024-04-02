from source.function_parts.integral_part import integral_part


class spatial_part(integral_part):
    def __init__(self):
        self.permutation_group : int = 0
        self.behavior = None
        self.choices_for_quantum_number_ml : dict = {}

    def print(self):
        pass

    def to_text(self):
        pass

    def find_all_choices(self):
        pass

    def get_spatial_part(self):
        pass