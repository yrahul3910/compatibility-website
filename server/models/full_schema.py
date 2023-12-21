from typing import List, Literal, Optional

from pydantic import BaseModel

from server.models import Range


class CenterRepel(BaseModel):
    factor: float


class CenterRepel01(BaseModel):
    factor: float


class Multiply(BaseModel):
    factor: float


class AddIfHigher(BaseModel):
    threshold: float
    add: float


class PostprocessOperator(BaseModel):
    type: Literal["center_repel_01"]

    center_repel_01: Optional[CenterRepel01]


class MergeOperator(BaseModel):
    type: Literal["multiply", "add_if_higher"]

    multiply: Optional[Multiply] = Multiply(factor=1.0)
    add_if_higher: Optional[AddIfHigher] = AddIfHigher(threshold=1, add=0)


class FuzzyMatch(BaseModel):
    reference: List[str]
    type: str = "CLUSTERING"


class LLMProximity(BaseModel):
    query: str


class EnumSpec(BaseModel):
    mapping: dict[str, float]


class Comparator(BaseModel):
    type: Literal["in_range", "fuzzy_match", "llm_proximity", "center_repel", "enum_pref"]
    postprocess: Optional[PostprocessOperator] = None
    merge: Optional[MergeOperator]

    # Optional fields, from type
    # See https://docs.pydantic.dev/2.5/migration/#required-optional-and-nullable-fields
    in_range: Optional[Range] = Range(min=0, max=1)
    center_repel: Optional[CenterRepel] = CenterRepel(factor=1.0)
    fuzzy_match: Optional[FuzzyMatch] = FuzzyMatch(reference=["Taylor Swift"])  # if there is no reference, I decide
    llm_proximity: Optional[LLMProximity] = LLMProximity(query="Reply with the number 1.")
    enum_pref: Optional[EnumSpec] = EnumSpec(mapping={"Yes": 1.0, "No": 0.0})


class Question(BaseModel):
    display: str
    key: str
    type: str
    range: Optional[Range] = None
    match: Optional[Comparator] = None

    enum: Optional[List[str]] = ["Yes", "No"]


class Schema(BaseModel):
    version: str
    questions: List[Question]
