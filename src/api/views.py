from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from http import HTTPStatus
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from datetime import date

from .serializers import QuestionSerializer, AnswerSerializer, DailySolutionSerializer
from .models import DailySolution as DailySolutionModel

POSSIBLE_ANSWERS = ["yes.", "no."]


# Create your views here.
class Question(views.APIView):
    serializer_class = QuestionSerializer

    @extend_schema(
        request=QuestionSerializer,
        auth=None,
        responses={
            HTTPStatus.OK: AnswerSerializer,
        },
        examples=[
            OpenApiExample(
                "With context request",
                request_only=True,
                value={
                    "country": "Brazil",
                    "question": "Is this country in South America?",
                    "context": [
                        {
                            "text": "Is this country beautiful?",
                            "is_user": True,
                        },
                        {
                            "text": "Yes.",
                            "is_user": False,
                        },
                    ],
                },
            ),
            OpenApiExample(
                "No context request",
                request_only=True,
                value={
                    "country": "Brazil",
                    "question": "Is this country in South America?",
                },
            ),
            OpenApiExample(
                "Yes response",
                response_only=True,
                status_codes=[HTTPStatus.OK],
                value={
                    "answer": "Yes.",
                },
            ),
            OpenApiExample(
                "No response",
                response_only=True,
                status_codes=[HTTPStatus.OK],
                value={
                    "answer": "No.",
                },
            ),
            OpenApiExample(
                "I can not answer that response",
                response_only=True,
                status_codes=[HTTPStatus.OK],
                value={
                    "answer": "I can not answer that.",
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


class DailySolution(views.APIView):
    @extend_schema(
        auth=None,
        responses={
            HTTPStatus.OK: DailySolutionSerializer,
        },
        examples=[
            OpenApiExample(
                "Normal request",
                response_only=True,
                status_codes=[HTTPStatus.OK],
                value={
                    "id": 1,
                    "solution": "Brazil",
                    "date": "2021-08-31",
                },
            ),
        ],
    )
    def get(self, request):
        """
        An API endpoint that returns the solution that is changed daily.
        """
        solution = DailySolutionModel.objects.get_or_create(date=date.today())[0]

        response_serializer = DailySolutionSerializer(solution)
        return Response(response_serializer.data, status=HTTPStatus.OK)
