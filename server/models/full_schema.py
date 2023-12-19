from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict

from server.models import Range


class PostprocessOperator(BaseModel):
    type: Literal["center_repel_01"]

    model_config = ConfigDict(
        extra="allow"
    )


class MergeOperator(BaseModel):
    type: Literal["multiply", "add_if_higher"]

    model_config = ConfigDict(
        extra="allow"
    )


class CenterRepel(BaseModel):
    factor: float


class FuzzyMatch(BaseModel):
    reference: List[str]


class Comparator(BaseModel):
    type: Literal["in_range", "fuzzy_match", "llm_proximity", "center_repel", "enum_pref"]
    postprocess: Optional[PostprocessOperator] = None
    merge: Optional[MergeOperator]

    # Optional fields, from type
    # See https://docs.pydantic.dev/2.5/migration/#required-optional-and-nullable-fields
    in_range: Optional[Range] = Range(min=0, max=1)
    center_repel: Optional[CenterRepel] = CenterRepel(factor=1.0)
    fuzzy_match: Optional[FuzzyMatch] = FuzzyMatch(reference=["Taylor Swift"])  # if there is no reference, I decide


class Question(BaseModel):
    display: str
    key: str
    type: str
    range: Optional[Range] = None
    match: Optional[Comparator] = None


class Schema(BaseModel):
    version: str
    questions: List[Question]
