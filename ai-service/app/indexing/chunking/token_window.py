from dataclasses import dataclass


@dataclass(slots=True)
class TokenWindow:

    token_start: int

    token_end: int

    token_ids: list[int]

    @property
    def token_count(self) -> int:
        return len(self.token_ids)