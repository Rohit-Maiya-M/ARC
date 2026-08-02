from dataclasses import dataclass


@dataclass(slots=True)
class RepositoryFile:
    repository_id: str
    repository_name: str

    file_id: str
    file_name: str

    relative_path: str
    extension: str

    content: str