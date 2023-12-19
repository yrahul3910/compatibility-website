import numpy as np
from openai import OpenAI

from server.models import Question


def fuzzy_match(question: Question, value: str) -> float:
    """
    Perform a fuzzy match between value and question.match.fuzzy_match.reference.

    :param question: The question.
    :param value: The value.
    :return: A score.
    """
    comparator = question.match

    if comparator is None:
        raise AssertionError(f"In question {question.key}, comparator is None")

    if comparator.type != "fuzzy_match":
        raise ValueError(f"Comparator type mismatch: {comparator.type} != fuzzy_match")

    if "fuzzy_match" not in comparator.model_fields or comparator.fuzzy_match is None:
        raise ValueError(f"Comparator missing fuzzy_match field: {comparator}")

    if "reference" not in comparator.fuzzy_match.model_fields or comparator.fuzzy_match.reference is None:
        raise ValueError(f"Comparator missing fuzzy_match.reference field: {comparator}")

    reference: list = comparator.fuzzy_match.reference

    if len(reference) == 0:
        raise ValueError(f"Comparator fuzzy_match.reference is empty: {comparator}")

    # Embed value, and all strings in reference.
    client = OpenAI()
    value_embedding = np.array(client.embeddings.create(
        input=value,
        model="text-embedding-ada-002"
    ).data[0].embedding)

    reference_embeddings = [np.array(client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    ).data) for text in reference]

    # Compute similarity
    similarity = [float(np.linalg.norm(value_embedding - reference_embedding, ord=2))
                  for reference_embedding in reference_embeddings]

    return max(similarity)
