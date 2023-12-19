from server.match.comparators import Matcher
from server.models import Schema, SurveyResponse


def match(survey: Schema, response: SurveyResponse) -> float:
    """
    Match a survey response to a schema.

    :param survey: The survey schema.
    :param response: The survey response.
    :return: A match score.
    """
    score: float = 1.0

    if survey.version != response.version:
        raise ValueError(f"Version mismatch: {survey.version} != {response.version}")

    for answer in response.responses:
        question = next(q for q in survey.questions if q.key == answer.key)

        # If the question's match is None, ignore
        if question.match is None:
            continue

        # If the type is "int" or "float", clip it to the range.
        if question.type in ["int", "float"]:
            if "range" not in question.model_fields or question.range is None:
                raise ValueError(f"Range missing from question: {question}")

            answer.value = float(max(question.range.min, min(question.range.max, float(answer.value))))

        matcher = Matcher(question, answer.value, score)
        score = matcher.apply()

    return score
