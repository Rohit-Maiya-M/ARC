from dataclasses import dataclass


@dataclass
class CodeSymbol:
    language: str

    symbol_name: str
    symbol_type: str
    symbol_path: str

    start_line: int
    start_column: int

    end_line: int
    end_column: int

    start_byte: int
    end_byte: int

    content: str