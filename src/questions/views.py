from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from http import HTTPStatus
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from .serializers import QuestionSerializer, AnswerSerializer

POSSIBLE_ANSWERS = ["yes.", "no."]


# Create your views here.
class Question(views.APIView):
    serializer_class = QuestionSerializer

    @extend_schema(
        request=QuestionSerializer,
        responses={
            HTTPStatus.OK: AnswerSerializer,
            HTTPStatus.BAD_REQUEST: {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": ["answer"],
            },
        },
        auth=None,
        examples=[
            OpenApiExample(
                "Normal request",
                request_only=True,
                value={
                    "country": "Brazil",
                    "question": "Is this country in South America?",
                },
            ),
            OpenApiExample(
                "Normal response",
                response_only=True,
                status_codes=[HTTPStatus.OK],
                value={
                    "answer": "No.",
                },
            ),
            OpenApiExample(
                "Error response",
                response_only=True,
                status_codes=[HTTPStatus.BAD_REQUEST],
                value={
                    "answer": ["The answer is not allowed."],
                },
            ),
        ],
    )
    def post(self, request):
        """
        An API endpoint that receives a question from the user and returns an answer from the GPT-3 API.
        """
        request_serializer = QuestionSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        response = request_serializer.create(request_serializer.validated_data)

        response_serializer = AnswerSerializer(data={"answer": response})
        response_serializer.is_valid(raise_exception=True)

        return Response(response_serializer.validated_data, status=HTTPStatus.OK)
