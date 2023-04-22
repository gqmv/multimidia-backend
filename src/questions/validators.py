from rest_framework import serializers


def AnswerAllowedValidator(answer):
    """
    A validator that checks if the answer is allowed.
    """
    ALLOWED_ANSWERS = ["yes.", "no.", "i can not answer that."]
    if answer.lower() not in ALLOWED_ANSWERS:
        raise serializers.ValidationError("The answer is not allowed.")
