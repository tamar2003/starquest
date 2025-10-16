"""
Global exception handler middleware for Django.
Catches and logs all unhandled exceptions during request processing.
"""
from typing import Callable
from django.http import JsonResponse
import logging


logger = logging.getLogger(__name__)


class GlobalExceptionMiddleware:
    """Middleware to catch and log unhandled exceptions globally."""
    def __init__(
        self,
        get_response: Callable[
            [JsonResponse],
            JsonResponse
        ]
    ) -> None:
        self.get_response = get_response

    def __call__(self, request: JsonResponse) -> JsonResponse:
        try:
            return self.get_response(request)
        except Exception:
            logger.exception("Unhandled exception in request.")
            return JsonResponse(
                {"error": "Internal server error."},
                status=500
            )
