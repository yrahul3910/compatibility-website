from server.models import Question


def enum_pref(question: Question, value: str) -> float:
    """
    Perform a enum preference match between value and question.match.enum_pref.reference.

    :param question: The question.
    :param value: The value.
    :return: A score.
    """
    comparator = question.match

    if question.type != "enum":
        raise ValueError(f"Question type mismatch: {question.type} != enum")
    if "enum" not in question.model_fields or question.enum is None:
        raise ValueError(f"Question missing enum field: {question}")

    if comparator is None:
        raise AssertionError(f"In question {question.key}, comparator is None")
    if comparator.type != "enum_pref":
        raise ValueError(f"Comparator type mismatch: {comparator.type} != enum_pref")

    if "enum_pref" not in comparator.model_fields or comparator.enum_pref is None:
        raise ValueError(f"Comparator missing enum_pref field: {comparator}")
    if "mapping" not in comparator.enum_pref.model_fields or comparator.enum_pref.mapping is None:
        raise ValueError(f"Comparator missing enum_pref.mapping field: {comparator}")

    mapping: dict = comparator.enum_pref.mapping

    if set(mapping.keys()) != set(question.enum):
        raise ValueError(f"Comparator enum_pref.mapping does not match question enum: {comparator}")

    if len(mapping) == 0:
        raise ValueError(f"Comparator enum_pref.mapping is empty: {comparator}")

    if value not in mapping:
        raise ValueError(f"Value {value} is not in mapping: {mapping}")

    return mapping[value]
