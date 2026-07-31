from app.indexing.chunking.constants import MIN_CHUNK_SIZE
from app.indexing.chunking.token_window import TokenWindow


class SemanticChunker:
    """
    Applies semantic optimizations to token windows before they are
    converted into CodeChunks.
    """

    def optimize(
        self,
        token_ids: list[int],
        windows: list[TokenWindow],
    ) -> list[TokenWindow]:
        """
        Optimize a list of TokenWindows.
        """

        if len(windows) <= 1:
            return windows

        return self._merge_last_small_window(
            token_ids,
            windows,
        )

    def _merge_last_small_window(
        self,
        token_ids: list[int],
        windows: list[TokenWindow],
    ) -> list[TokenWindow]:
        """
        Merge the final window into the previous one if it is too small.
        """

        last = windows[-1]

        if last.token_count >= MIN_CHUNK_SIZE:
            return windows

        previous = windows[-2]

        merged_window = TokenWindow(
            token_start=previous.token_start,
            token_end=last.token_end,
            token_ids=token_ids[
                previous.token_start:last.token_end
            ],
        )

        return windows[:-2] + [merged_window]