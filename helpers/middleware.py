import json
import logging

from datetime import datetime

from fastapi import HTTPException
from sqlmodel import select
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from database.db_session import get_db
from database.models import AuditLog, User
from helpers.auth import get_current_user

logger = logging.getLogger(__name__)

EXCLUDED_FIELDS = {"password", "access_token", "refresh_token"}


class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        path = request.url.path
        timestamp = datetime.utcnow()

        # Capture Request Body
        request_body = await request.body()
        request_body_text = request_body.decode("utf-8") if request_body else None


        if request_body_text is not None:
            try:
                json_request_body = json.loads(request_body_text)
                filtered_request_body = {k: v for k, v in json_request_body.items() if k not in EXCLUDED_FIELDS}
                filtered_request_body_text = json.dumps(filtered_request_body)
            except json.JSONDecodeError:
                logger.error(f"Failed to decode JSON from request body: {request_body_text}")
                filtered_request_body_text = ""
        else:
            filtered_request_body_text = ""



        # Capture Response Data
        try:
            response = await call_next(request)
            error_message = None
        except HTTPException as e:
            logger.error(f"HTTPException: caught in middleware: {e}")
            response = await self.handle_exception(e)
            error_message = e.detail

        response_body = b"".join([chunk async for chunk in response.body_iterator])
        response_body_text = response_body.decode("utf-8")

        filtered_response_body_text = ""
        if path == "/token":
            try:
                json_response_body = json.loads(response.body)
                filtered_response_body = {k: v for k, v in json_response_body.items() if
                                 k not in EXCLUDED_FIELDS}  # Filter out tokens
                filtered_response_body_text = json.dumps(filtered_response_body)
            except Exception:
                pass  # If we can't process response body, skip
        else:
            filtered_response_body_text = response_body_text

        # Get User ID
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            username = get_current_user(token)
            user = next(get_db()).execute(select(User).where(User.username == username)).scalar_one_or_none()
        else:
            user = None

        # Log the data to the database
        session = next(get_db())
        log_entry = AuditLog(
            method=method,
            path=path,
            timestamp=timestamp,
            request_body=filtered_request_body_text,
            response_body=filtered_response_body_text,
            status_code=response.status_code,
            user_id=user.id if user is not None else None,
            error_message=error_message
        )
        session.add(log_entry)
        session.commit()

        # Log request and response
        logger.debug(f"Request - Method: {method}, Path: {path}, Body: {request_body_text}")
        logger.debug(f"Response - Status: {response.status_code}, Body: {response_body_text}")

        # Return the response with the captured body
        return Response(content=response_body, status_code=response.status_code, headers=dict(response.headers),
                        media_type=response.media_type)

    async def handle_exception(self, exc: HTTPException):
        """Handle exceptions raised during request processing."""
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

