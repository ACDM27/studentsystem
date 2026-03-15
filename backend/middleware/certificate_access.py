"""
Middleware for controlling access to certificate files
Only allows students to access their own certificates, or admins to access all
"""

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import re

from config import settings
from auth import decode_access_token
from database import SessionLocal
from models import SysUser, UserRole


class CertificateAccessMiddleware(BaseHTTPMiddleware):
    """Middleware to control access to certificate files"""

    async def dispatch(self, request: Request, call_next) -> Response:
        # Only intercept requests for certificate files
        if not request.url.path.startswith("/uploads/certificates/"):
            return await call_next(request)

        # Extract student ID from path
        # Path format: /uploads/certificates/student_{id}/cert_xxx.jpg
        match = re.match(r"/uploads/certificates/student_(\d+)/", request.url.path)

        if not match:
            return JSONResponse(
                status_code=404,
                content={"detail": "Certificate not found"}
            )

        file_owner_id = int(match.group(1))

        # Get authorization token
        # Priority: Authorization header > URL query param ?token=xxx > cookie
        # Note: Browser <img> tags cannot set Authorization header,
        # so we support token via URL query param as fallback
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "")
        else:
            # Fallback: try URL query param ?token=xxx (for img tag direct access)
            token = request.query_params.get("token")
            if not token:
                # Last resort: check cookie
                token = request.cookies.get("access_token")
            if not token:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Authentication required to access certificates"}
                )

        # Decode token and verify access
        try:
            payload = decode_access_token(token)
            user_id = payload.get("sub")

            if not user_id:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid token"}
                )

            # Get user from database
            db = SessionLocal()
            try:
                user = db.query(SysUser).filter(SysUser.id == int(user_id)).first()

                if not user:
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "User not found"}
                    )

                # Check access permissions
                # Admin can access all certificates
                if user.role == UserRole.ADMIN:
                    pass  # Allow access
                # Student can only access their own certificates
                elif user.role == UserRole.STUDENT:
                    if user.student and user.student.id == file_owner_id:
                        pass  # Allow access
                    else:
                        return JSONResponse(
                            status_code=403,
                            content={"detail": "Access denied: You can only access your own certificates"}
                        )
                else:
                    return JSONResponse(
                        status_code=403,
                        content={"detail": "Access denied"}
                    )

            finally:
                db.close()

        except Exception as e:
            return JSONResponse(
                status_code=401,
                content={"detail": f"Authentication failed: {str(e)}"}
            )

        # Token valid and access granted — continue request
        return await call_next(request)
