from server.match.comparators import Comparator


def in_range(comparator: Comparator, value: float, score: float):
    """
    Match a value to a range.

    :param comparator: The comparator.
    :param value: The value.
    :param score: The current score.
    :return: A new score.
    """
    assert comparator.type == "in_range"
    assert "in_range" in comparator.__fields__

    return comparator.in_range.min <= value <= comparator.in_range.max
