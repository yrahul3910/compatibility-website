"""
A parser that converts a schema to a JSON to be sent to the front-end
"""

from typing import List

from pydantic import ValidationError

from server.models import Question, ReducedQuestion, ReducedSchema, Schema


def schema_to_json(input: dict) -> ReducedSchema:
    """
    Converts a schema to a JSON to be sent to the front-end.

    :param schema: The schema to be converted
    :return: The converted schema
    """
    try:
        schema = Schema(**input)

        questions: List[Question] = schema.questions
        reduced_questions: List[ReducedQuestion] = [ReducedQuestion(
                display=q.display,
                key=q.key,
                type=q.type,
                range=q.range)
            for q in questions]

        return ReducedSchema(version=schema.version, questions=reduced_questions)
    except ValidationError as e:
        print(e)
        raise
