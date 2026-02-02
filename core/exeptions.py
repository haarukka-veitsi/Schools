from rest_framework.exceptions import APIException


class NotFoundException(APIException):
    status_code = 404
    default_detail = "Object not found"


class InternalErrorException(APIException):
    status_code = 500
    default_detail = "Internal server error"
