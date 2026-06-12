from pydantic import BaseModel


class SummaryRequest(BaseModel):
    repository_id: int
