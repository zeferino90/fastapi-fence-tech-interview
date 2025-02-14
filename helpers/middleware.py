import logging
from datetime import datetime

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from database.db_session import get_db
from database.models import AuditLog

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        path = request.url.path
        timestamp = datetime.utcnow()

        # Capture Request Body
        request_body = await request.body()
        request_body_text = request_body.decode("utf-8") if request_body else None

        # Capture Response Data
        response = await call_next(request)
        response_body = b"".join([chunk async for chunk in response.body_iterator])
        response_body_text = response_body.decode("utf-8")

        # Log the data to the database
        session = next(get_db())
        log_entry = AuditLog(
            method=method,
            path=path,
            timestamp=timestamp,
            request_body=request_body_text,
            response_body=response_body_text,
            status_code=response.status_code,
        )
        session.add(log_entry)
        session.commit()

        # Log request and response
        logger.info(f"Request - Method: {method}, Path: {path}, Body: {request_body_text}")
        logger.info(f"Response - Status: {response.status_code}, Body: {response_body_text}")

        # Return the response with the captured body
        return Response(content=response_body, status_code=response.status_code, headers=dict(response.headers),
                        media_type=response.media_type)
