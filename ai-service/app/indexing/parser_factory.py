from app.indexing.parsers.base_parser import BaseParser
from app.indexing.parsers.java_parser import JavaParser


class ParserFactory:

    PARSERS = {
        "java": JavaParser,
    }

    @classmethod
    def create_parser(cls, language: str) -> BaseParser:

        parser = cls.PARSERS.get(language)

        if parser is None:
            raise ValueError(
                f"Unsupported language: {language}"
            )

        return parser()