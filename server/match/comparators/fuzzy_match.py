import os

import numpy as np
import vertexai
from dotenv import load_dotenv
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

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

    # Load variables from .env
    load_dotenv()

    # Check environment variables
    if "PROJECT_ID" not in os.environ:
        raise EnvironmentError("PROJECT_ID not in environment variables")
    if "REGION" not in os.environ:
        raise EnvironmentError("REGION not in environment variables")
    if "EMBEDDING_MODEL" not in os.environ:
        raise EnvironmentError("EMBEDDING_MODEL not in environment variables")

    # Set up Vertex AI
    vertexai.init(project=os.environ["PROJECT_ID"], location=os.environ["REGION"])

    # Embed value, and all strings in reference.
    model = TextEmbeddingModel.from_pretrained(os.environ["EMBEDDING_MODEL"])
    reference_inputs = [TextEmbeddingInput(text=value, task_type="CLUSTERING") for value in reference]
    value_input = TextEmbeddingInput(text=value, task_type="CLUSTERING")

    value_embedding = np.array(model.get_embeddings([value_input])[0].values)
    reference_embeddings = np.array(
        [model.get_embeddings([reference_input])[0].values for reference_input in reference_inputs]
    )

    # Compute similarity
    similarity = [float(np.linalg.norm(value_embedding - reference_embedding, ord=2))
                  for reference_embedding in reference_embeddings]

    return max(similarity)
