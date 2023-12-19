from server.models import Question


def in_range(question: Question, value: float) -> float:
    """
    Match a value to a range.

    :param question: The question.
    :param value: The answer.
    :return: A new score.
    """
    comparator = question.match

    if comparator is None:
        raise AssertionError(f"In question {question.key}, comparator is None")

    if comparator.type != "in_range":
        raise ValueError(f"Comparator type mismatch: {comparator.type} != in_range")

    if "in_range" not in comparator.model_fields or comparator.in_range is None:
        raise ValueError(f"Comparator missing in_range field: {comparator}")

    return float(comparator.in_range.min <= value <= comparator.in_range.max)
