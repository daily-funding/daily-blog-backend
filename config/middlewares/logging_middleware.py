import logging
import time

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        self.do_request_log(request)

        response = self.get_response(request)

        duration = (time.time() - start) * 1000
        self.do_response_log(duration, request, response)

        return response

    def do_request_log(self, request):
        logger.info(
            "REQUEST method=%s path=%s ip=%s",
            request.method,
            request.path,
            self._get_client_ip(request),
        )

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "-")

    def do_response_log(self, duration, request, response):
        logger.info(
            "RESPONSE method=%s path=%s status=%s duration=%.1fms",
            request.method,
            request.path,
            response.status_code,
            duration,
        )
