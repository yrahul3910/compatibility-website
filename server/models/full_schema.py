from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict

from server.models import Range


class PostprocessOperator(BaseModel):
    type: Literal["center_repel"]

    model_config = ConfigDict(
        extra="allow"
    )


class MergeOperator(BaseModel):
    type: Literal["multiply", "add_if_higher"]

    model_config = ConfigDict(
        extra="allow"
    )


class Comparator(BaseModel):
    type: Literal["in_range", "fuzzy_match", "llm_proximity", "center_repel", "enum_pref"]
    postprocess: Optional[PostprocessOperator] = None
    merge: Optional[MergeOperator]

    model_config = ConfigDict(
        extra="allow"
    )


class Question(BaseModel):
    display: str
    key: str
    type: str
    range: Optional[Range] = None
    match: Optional[Comparator] = None


class Schema(BaseModel):
    version: str
    questions: List[Question]
