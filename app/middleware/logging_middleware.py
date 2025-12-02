import logging

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            logger.info(
                f"{request.method} {request.url.path} "
                f"status={response.status_code} "
                f"time={process_time:.3f}s"
            )
            return response

        except Exception as e:
            process_time = time.time() - start_time

            logger.exception(
                f"Exception on {request.method} {request.url.path} "
                f"after {process_time:.3f}s"
            )
            raise
