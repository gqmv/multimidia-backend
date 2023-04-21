from rest_framework.exceptions import APIException


class InvalidAnswerException(APIException):
    def __init__(self, message):
        super().__init__(message)
