from abc import ABC, abstractmethod


class IntegralPart(ABC):
    """ general class for integrals of different kind (only used as a parent, not on its own) """

    @abstractmethod
    def to_text(self):
        pass

    @abstractmethod
    def to_tex(self) -> str:
        pass
