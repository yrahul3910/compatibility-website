from typing import List

from pydantic import BaseModel


class Answer(BaseModel):
    """
    An answer to a question.
    """
    key: str
    value: str


class SurveyResponse(BaseModel):
    """
    A survey response.
    """
    version: str
    responses: List[Answer]
