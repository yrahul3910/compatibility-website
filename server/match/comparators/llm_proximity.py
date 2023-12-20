import os
import re

import vertexai
from dotenv import load_dotenv
from vertexai.preview.generative_models import GenerationConfig, GenerationResponse, GenerativeModel

from server.models import Question


def llm_proximity(question: Question, value: str) -> float:
    """
    Proximity using an LLM query.

    :param question: The question.
    :param value: The answer.
    :return: A new score.
    """
    comparator = question.match

    if comparator is None:
        raise AssertionError(f"In question {question.key}, comparator is None")
    if comparator.type != "llm_proximity":
        raise ValueError(f"Comparator type mismatch: {comparator.type} != llm_proximity")

    if "llm_proximity" not in comparator.model_fields or comparator.llm_proximity is None:
        raise ValueError(f"Comparator missing llm_proximity field: {comparator}")
    if "query" not in comparator.llm_proximity.model_fields or comparator.llm_proximity.query is None:
        raise ValueError(f"Comparator missing llm_proximity.query field: {comparator}")

    # Load variables from .env
    load_dotenv()

    # Check environment variables
    if "PROJECT_ID" not in os.environ:
        raise EnvironmentError("PROJECT_ID not in environment variables")
    if "REGION" not in os.environ:
        raise EnvironmentError("REGION not in environment variables")
    if "LLM_MODEL" not in os.environ:
        raise EnvironmentError("LLM_MODEL not in environment variables")

    query = comparator.llm_proximity.query.replace("$value", value)

    # Set up Vertex AI
    vertexai.init(project=os.environ["PROJECT_ID"], location=os.environ["REGION"])

    # Generate text
    model = GenerativeModel(os.environ["LLM_MODEL"])
    config = GenerationConfig(
        temperature=0.8,  # lower values make it more deterministic
        top_k=10,  # higher values make it choose more probable words
        top_p=0.9,  # allows some diversity in the output
    )
    prompt = f"""
    Answer the following question with a real number between 0 and 1. Do not elaborate on your answer.
    Reply with only a number.

    {query}
    """
    response_object = model.generate_content(prompt, generation_config=config, stream=False)
    if response_object is None:
        raise RuntimeError("LLM response is None")

    assert isinstance(response_object, GenerationResponse)

    response: str = response_object.text

    # Just in case, use regex to find a floating point number in the response
    match = re.search(r"[-+]?\d*\.\d+|\d+", response)
    if match is None:
        raise RuntimeError(f"LLM response does not contain a number: {response}")

    return float(match.group(0))
