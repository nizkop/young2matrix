from typing import List


def calculate_spin_quantum_numbers(number_of_particles:int, single_particle_spin:float=1/2) -> List[float]:
    """
    calculates total spin: S = { |s1 - s_2 - ... - s_i| , |s1 - s2 - ... - si| +1, ... , (s1 + ... + si) }
    :param single_particle_spin: spin choices as absolute value (plus & minus), default set to electrons (float with at most 1 decimal place)
    :param number_of_particles: needed as i in equation above
    :return: list of total spin possibilities (floats with at most 1 decimal place)
    """
    spin = single_particle_spin - (number_of_particles - 1) * single_particle_spin
    spins = []
    while spin <= (number_of_particles * single_particle_spin):
        spins.append(abs(spin))
        spin += 1
    return list(set(spins))