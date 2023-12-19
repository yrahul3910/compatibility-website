from typing import List

from pydantic import BaseModel

from server.models import Number


class Answer(BaseModel):
    """
    An answer to a question.
    """
    key: str
    value: Number | str


class SurveyResponse(BaseModel):
    """
    A survey response.
    """
    version: str
    responses: List[Answer]
