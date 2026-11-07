import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.access")


def get_client_ip(request: Request) -> str:
    """
    Get client IP safely.

    Trust X-Forwarded-For only when the application
    is behind a trusted reverse proxy.
    """

    forwarded_for = request.headers.get("X-Forwarded-For")

    if forwarded_for:
        # First IP is the original client in a correctly
        # configured trusted proxy chain.
        return forwarded_for.split(",")[0].strip()

    if request.client:
        return request.client.host

    return "unknown"


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()

        client_ip = get_client_ip(request)

        method = request.method
        path = request.url.path

        request.state.request_id = request_id

        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code

            response.headers["X-Request-ID"] = request_id

            return response

        except Exception:
            logger.exception(
                "Request failed | request_id=%s",
                request_id,
            )
            raise

        finally:
            duration = (time.perf_counter() - start_time) * 1000

            logger.info(
                "Request | "
                "request_id=%s | "
                "ip=%s | "
                "method=%s | "
                "path=%s | "
                "status=%s | "
                "duration=%.2fms",
                request_id,
                client_ip,
                method,
                path,
                status_code,
                duration,
            )