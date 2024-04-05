from typing import List


def calculate_ms_quantum_number(total_spin:float) -> List[float]:
    """  calculating m_S = { -max(S), -max(S)+1, ..., 0, ..., max(S) }
     :param spin: total spin (float with at most 1 decimal place)
     :return: possibilites for quantum number ms (floats with at most 1 decimal place)
     """
    total_spin=abs(total_spin) # just to be sure
    ms_values = []
    current_ms = -total_spin
    while current_ms <= total_spin:
        ms_values.append(current_ms)
        current_ms += 1
    return list(set(ms_values))
