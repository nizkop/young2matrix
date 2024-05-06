from source.function_parts.text_kinds import text_kinds


def get_dirac_notation(bra: str, ket: str, kind: text_kinds) -> str:
    """ textual building of integral in dirac notation
    :param bra: equation part for the bra
    :param ket: equation part in the ket
    :param kind: choice between text and latex format
    :return: equation with bra and ket
    """
    if kind == text_kinds.TEX:
        return r"\bra{\," + bra + r"\,} \ket{\," + ket + r"\,}"
    return f"< {bra} | {ket} >"
