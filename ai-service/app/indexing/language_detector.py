from pathlib import Path


class LanguageDetector:

    EXTENSION_MAP = {
        ".java": "java",
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".go": "go",
        ".rs": "rust",
        ".kt": "kotlin",
        ".cs": "csharp",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".cxx": "cpp",
        ".hpp": "cpp",
        ".c": "c",
        ".h": "c",
        ".swift": "swift",
    }

    FILE_NAME_MAP = {
        "Dockerfile": "dockerfile",
        "Makefile": "makefile",
        "Jenkinsfile": "groovy",
    }

    @classmethod
    def detect(cls, file_name: str) -> str |None:

        name = Path(file_name).name

        if name in cls.FILE_NAME_MAP:
            return cls.FILE_NAME_MAP[name]

        extension = Path(file_name).suffix.lower()

        return cls.EXTENSION_MAP.get(extension)