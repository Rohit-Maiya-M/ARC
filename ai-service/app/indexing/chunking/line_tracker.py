from bisect import bisect_right


class LineTracker:
    """
    Maps token windows back to source-code line numbers using the
    tokenizer's offset_mapping.
    """

    def get_line_range(
        self,
        text: str,
        offset_mapping: list[tuple[int, int]],
        token_start: int,
        token_end: int,
    ) -> tuple[int, int]:
        """
        Returns the (start_line, end_line) for a token window.

        Parameters
        ----------
        text:
            Original source code.

        offset_mapping:
            HuggingFace tokenizer offset mapping.
            Each element is (start_char, end_char).

        token_start:
            Inclusive token index.

        token_end:
            Exclusive token index.
        """

        if not text:
            return (1, 1)

        if not offset_mapping:
            return (1, 1)
        
        newline_positions = [
            index
            for index, ch in enumerate(text)
            if ch == "\n"
        ]
        
        start_char = offset_mapping[token_start][0]
        
        end_char = offset_mapping[token_end - 1][1]

        start_line = self._char_to_line(
            start_char,
            newline_positions,
        )

        end_line = self._char_to_line(
            end_char,
            newline_positions,
        )

        return start_line, end_line

    @staticmethod
    def _char_to_line(
        char_position: int,
        newline_positions: list[int],
    ) -> int:
        """
        Convert a character offset into a 1-based line number.
        """

        return bisect_right(
            newline_positions,
            char_position,
        ) + 1