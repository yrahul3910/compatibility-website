from server.models import MergeOperator


def multiply(merge: MergeOperator, matched_score: float, score: float):
    """
    Multiply the matched score by the score.

    :param merge: The merge operator.
    :param matched_score: The matched score.
    :param score: The score.
    :return: The multiplied score.
    """
    if merge.type != "multiply":
        raise ValueError(f"Merge type mismatch: {merge.type} != multiply")

    if "multiply" not in merge.model_fields or merge.multiply is None:
        raise ValueError(f"Merge missing multiply field: {merge}")

    return matched_score * score * merge.multiply.factor
