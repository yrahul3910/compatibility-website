from server.models import MergeOperator


def add_if_higher(merge: MergeOperator, matched_score: float, score: float):
    """
    Add an additional value to the score if it is higher than a threshold.

    :param merge: The merge operator.
    :param matched_score: The matched score.
    :param score: The score.
    :return: The multiplied score.
    """
    if merge.type != "add_if_higher":
        raise ValueError(f"Merge type mismatch: {merge.type} != add_if_higher")

    if "add_if_higher" not in merge.model_fields or merge.add_if_higher is None:
        raise ValueError(f"Merge missing add_if_higher field: {merge}")

    if matched_score > merge.add_if_higher.threshold:
        return score + merge.add_if_higher.add
    return score
