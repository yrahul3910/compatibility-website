from typing import Union

from pydantic import BaseModel

Number = Union[int, float]


class Range(BaseModel):
    min: Number
    max: Number
