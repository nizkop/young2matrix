from source.function_parts.FunctionDependency import FunctionDependency
from source.function_parts.IntegralPart import IntegralPart


class SpatialPart(IntegralPart):
    """
    class only needed for coherence, because spatial functions are the opposite of spin functions
    but spatial functions/orbitals are not specifically given here, so that spatial parts fall back to the general integral parts
    """
    def __init__(self, behavior:FunctionDependency):
        self.permutation_group : int = 0
        self.function = behavior
        self.choices_for_quantum_number_ml : dict = {}

    def to_tex(self) -> str:
        return self.function.to_tex()

    def to_text(self) -> str:
        return self.function.to_text()
