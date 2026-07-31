from abc import ABC, abstractmethod

from app.indexing.models.code_symbol import CodeSymbol


class BaseParser(ABC):

    @abstractmethod
    def parse(self, content: str) -> list[CodeSymbol]:
        """
        Parse a source file and return the extracted symbols.
        """
        pass