from source.function_parts.ttext_kinds import text_kinds


def get_dirac_notation(bra: str, ket: str, kind: text_kinds):
    """ textual building of integral """
    if kind == text_kinds.TEX:
        return r"\bra{\," + bra + r"\,} \ket{\," + ket + r"\,}"
    return f"< {bra} | {ket} >"
