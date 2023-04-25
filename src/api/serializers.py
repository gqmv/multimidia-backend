from rest_framework import serializers

from .validators import AnswerAllowedValidator
from .services import get_answer
from .countries import COUNTRIES
from .models import DailySolution


class MessageSerializer(serializers.Serializer):
    """
    This serializer is used to serialize a message instance.
    """

    text = serializers.CharField(max_length=100, required=True, write_only=True)
    is_user = serializers.BooleanField(required=True, write_only=True)


class QuestionSerializer(serializers.Serializer):
    """
    A serializer responsible for receiving data from a user question.
    """

    country = serializers.CharField(max_length=50, required=True, write_only=True)
    question = serializers.CharField(max_length=100, required=True, write_only=True)
    context = MessageSerializer(many=True, required=False, write_only=True)

    def create(self, validated_data: dict) -> str:
        return get_answer(
            country=validated_data["country"],
            question=validated_data["question"],
            context=validated_data.get("context", None),
        )


class AnswerSerializer(serializers.Serializer):
    """
    A serializer responsible for receiving data from a GPT response.
    """

    answer = serializers.CharField(
        max_length=50,
        required=True,
        validators=[AnswerAllowedValidator],
    )


class DailySolutionSerializer(serializers.ModelSerializer):
    """
    This serializer is used for sending the daily solution to the frontend.
    """

    class Meta:
        model = DailySolution
        fields = ["id", "solution", "date"]
        read_only_fields = ["id", "date", "solution"]
