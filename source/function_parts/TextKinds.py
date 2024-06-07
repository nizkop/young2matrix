from enum import Enum


class TextKinds(Enum):
    """ choosing between pure text display or latex format """
    TEX = "tex"
    TXT = "text"