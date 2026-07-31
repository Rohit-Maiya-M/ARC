from pathlib import Path


RESOURCE_ROOT = (
    Path(__file__).resolve().parents[1]
    / "resources"
)


def load_resource(
    language: str,
    filename: str,
) -> str:
    """
    Load a test resource from tests/resources.

    Example:
        load_resource("java", "Example.java")
    """

    file_path = (
        RESOURCE_ROOT
        / language
        / filename
    )

    return file_path.read_text(
        encoding="utf-8"
    )