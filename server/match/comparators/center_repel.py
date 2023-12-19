from server.models import Question


def center_repel(question: Question, value: float) -> float:
    """
    Repel value away from the center.

    :param question: The question.
    :param value: The answer.
    :return: A new score.
    """
    comparator = question.match

    if comparator is None:
        raise AssertionError(f"In question {question.key}, comparator is None")

    if comparator.type != "center_repel":
        raise ValueError(f"Comparator type mismatch: {comparator.type} != center_repel")

    if "center_repel" not in comparator.model_fields or comparator.center_repel is None:
        raise ValueError(f"Comparator missing center_repel field: {comparator}")

    if question.range is None:
        raise ValueError(f"Question missing range: {question.key}")

    center: float = question.range.min + (question.range.max - question.range.min) / 2
    distance: float = value - center

    return center + distance * comparator.center_repel.factor
