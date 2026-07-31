import time

from app.embeddings.embedder import Embedder
from app.indexing.chunking.symbol_chunker import SymbolChunker
from app.indexing.language_detector import LanguageDetector
from app.indexing.models.repository_file import RepositoryFile
from app.indexing.parser_factory import ParserFactory


class RepositoryIndexer:

    def __init__(self):

        self.chunker = SymbolChunker()
        self.embedder = Embedder()

    def index(
        self,
        repository_file: RepositoryFile,
    ):

        total_start = time.perf_counter()

        # ----------------------------------------
        # Language Detection
        # ----------------------------------------

        start = time.perf_counter()

        language = LanguageDetector.detect(
            repository_file.relative_path
        )

        language_time = time.perf_counter() - start

        # ----------------------------------------
        # Parser Creation
        # ----------------------------------------

        start = time.perf_counter()

        parser = ParserFactory.create_parser(
            language
        )

        parser_creation_time = time.perf_counter() - start

        # ----------------------------------------
        # Parsing
        # ----------------------------------------

        start = time.perf_counter()

        symbols = parser.parse(
            repository_file.content
        )

        parsing_time = time.perf_counter() - start

        # ----------------------------------------
        # Chunking
        # ----------------------------------------

        start = time.perf_counter()

        chunks = self.chunker.chunk(
            repository_file=repository_file,
            symbols=symbols,
        )

        chunking_time = time.perf_counter() - start

        # ----------------------------------------
        # Embedding
        # ----------------------------------------

        start = time.perf_counter()

        embedded_chunks = self.embedder.embed_chunks(
            chunks
        )

        embedding_time = time.perf_counter() - start

        total_time = time.perf_counter() - total_start

        print("\n" + "=" * 70)
        print("Repository Indexing Performance")
        print("=" * 70)
        print(f"Language Detection : {language_time:.4f} sec")
        print(f"Parser Creation    : {parser_creation_time:.4f} sec")
        print(f"Parsing            : {parsing_time:.4f} sec")
        print(f"Chunking           : {chunking_time:.4f} sec")
        print(f"Embedding          : {embedding_time:.4f} sec")
        print("-" * 70)
        print(f"Symbols            : {len(symbols)}")
        print(f"Chunks             : {len(chunks)}")
        print(f"Embedded Chunks    : {len(embedded_chunks)}")
        print("-" * 70)
        print(f"Total              : {total_time:.4f} sec")
        print("=" * 70)

        return embedded_chunks