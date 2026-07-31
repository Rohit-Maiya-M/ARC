import hashlib


def sha256(content: str) -> str:
    """
    Compute the SHA-256 hash of a string.
    """

    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()