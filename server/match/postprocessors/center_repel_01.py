from server.models.full_schema import PostprocessOperator


def center_repel_01(postprocessor: PostprocessOperator, score: float) -> float:
    """
    Center-repel a score to the range [0, 1].

    :param postprocessor: The postprocessor operator.
    :param score: The score.
    :return: The center-repelled score.
    """
    if postprocessor.type != "center_repel_01":
        raise ValueError(f"Postprocessor type mismatch: {postprocessor.type} != center_repel_01")

    if "center_repel_01" not in postprocessor.model_fields or postprocessor.center_repel_01 is None:
        raise ValueError(f"Postprocessor missing center_repel_01 field: {postprocessor}")

    center = 0.5
    factor = postprocessor.center_repel_01.factor
    distance = score - center

    return center + distance * factor
