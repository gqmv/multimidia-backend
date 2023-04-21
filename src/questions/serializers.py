from rest_framework import serializers

from .validators import AnswerAllowedValidator
from .services import get_answer


class GPTPromptSerializer(serializers.Serializer):
    """
    A serializer responsible for receiving data from a user question.
    """

    country = serializers.CharField(max_length=50, required=True, write_only=True)
    question = serializers.CharField(max_length=100, required=True, write_only=True)

    def create(self, validated_data: dict) -> str:
        response = get_answer(validated_data["country"], validated_data["question"])
        return response


class GPTResponseSerializer(serializers.Serializer):
    """
    A serializer responsible for receiving data from a GPT response.
    """

    answer = serializers.CharField(
        max_length=50,
        required=True,
        validators=[AnswerAllowedValidator],
    )
