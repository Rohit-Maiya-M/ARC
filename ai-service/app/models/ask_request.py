from pydantic import BaseModel

class AskRequest(
    BaseModel
):
    question: str

    repository_id: int