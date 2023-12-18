from typing import List, Optional

from pydantic import BaseModel

from server.models import Range


class ReducedQuestion(BaseModel):
    display: str
    key: str
    type: str
    range: Optional[Range] = None


class ReducedSchema(BaseModel):
    version: str
    questions: List[ReducedQuestion]
