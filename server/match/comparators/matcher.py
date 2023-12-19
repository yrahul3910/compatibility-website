# ruff: noqa: F821
# The above is temporary
from server.match.comparators import center_repel, fuzzy_match, in_range
from server.models import Number, Question


class Matcher:
    AVAILABLE_COMPARATORS = {
        "in_range": in_range,
        "fuzzy_match": fuzzy_match,
        "llm_proximity": llm_proximity,
        "center_repel": center_repel,
        "enum_pref": enum_pref,
    }
    AVAILABLE_POSTPROCESSORS = {
        "center_repel_01": center_repel_01
    }
    AVAILABLE_MERGERS = {
        "multiply": multiply,
        "add_if_higher": add_if_higher
    }

    def __init__(self, question: Question, value: Number | str, score: float):
        if question.match is None:
            raise ValueError(f"In question {question.key}, comparator is None")

        if question.match.type not in self.AVAILABLE_COMPARATORS:
            raise ValueError(
                f"Invalid comparator: {question.match.type} not in {self.AVAILABLE_COMPARATORS.keys()}")

        self.score = score
        self.value = value
        self.question = question

    def apply(self):
        comparator = self.question.match

        if comparator is None:
            raise AssertionError(f"In question {self.question.key}, comparator is None")

        if comparator.merge is None:
            return self.score

        matched_score = self.AVAILABLE_COMPARATORS[comparator.type](self.question, self.value)

        if comparator.postprocess is not None:
            operator_name = comparator.postprocess.type
            matched_score = self.AVAILABLE_POSTPROCESSORS[operator_name](matched_score)

        self.AVAILABLE_MERGERS[comparator.merge.type](comparator.merge, matched_score, self.score)

        return matched_score
