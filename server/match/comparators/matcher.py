# ruff: noqa: F821
# The above is temporary
from server.match.comparators import Comparator
from server.match.comparators.in_range import in_range
from server.models import Number


class Matcher:
    AVAILABLE_COMPARATORS = {
        "in_range": in_range,
        "fuzzy_match": fuzzy_match,
        "llm_proximity": llm_proximity,
        "center_repel": center_repel,
        "enum_pref": enum_pref,
    }
    AVAILABLE_POSTPROCESSORS = {
        "center_repel": center_repel
    }
    AVAILABLE_MERGERS = {
        "multiply": multiply,
        "add_if_higher": add_if_higher
    }

    def __init__(self, comparator: Comparator, value: Number, score: float):
        assert comparator.type in self.AVAILABLE_COMPARATORS

        self.score = score
        self.value = value
        self.comparator = comparator

    def apply(self):
        if self.comparator.merge is None:
            return self.score

        matched_score = self.AVAILABLE_COMPARATORS[self.comparator.type](self.comparator, self.value)

        if self.comparator.postprocess is not None:
            operator_name = self.comparator.postprocess.type
            matched_score = self.AVAILABLE_POSTPROCESSORS[operator_name](self.comparator.postprocess, matched_score)

        self.AVAILABLE_MERGERS[self.comparator.merge.type](self.comparator.merge, matched_score)

        return matched_score
