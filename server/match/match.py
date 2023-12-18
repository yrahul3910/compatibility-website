from server.match.comparators import Matcher
from server.models import Comparator, Schema, SurveyResponse


def match(survey: Schema, response: SurveyResponse) -> float:
    """
    Match a survey response to a schema.

    :param survey: The survey schema.
    :param response: The survey response.
    :return: A match score.
    """
    score: float = 1.0

    assert survey.version == response.version

    for answer in response.responses:
        question = next(q for q in survey.questions if q.key == answer.key)

        # If the question's match is None, ignore
        if question.match is None:
            continue

        # If the type is "int" or "float", clip it to the range.
        if question.type in ["int", "float"]:
            answer.value = float(max(question.range.min, min(question.range.max, float(answer.value))))

        comparator: Comparator = question.match
        matcher = Matcher(comparator, answer.value, score)
        score = matcher.apply()
