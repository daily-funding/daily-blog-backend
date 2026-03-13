from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.views import exception_handler

from blog.exceptions import BlogException


def custom_exception_handler(exc, context):

    if isinstance(exc, BlogException):
        return handle_blog_exceptions(exc, context)

    # DRF 기본 핸들러
    response = exception_handler(exc, context)
    if response is not None:
        return response

    return Response(
        {"error": "서버 오류가 발생했습니다."}, status=HTTP_500_INTERNAL_SERVER_ERROR
    )


def handle_blog_exceptions(exc, context):
    return Response({"error": str(exc)}, status=HTTP_400_BAD_REQUEST)
