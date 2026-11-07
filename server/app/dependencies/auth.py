
from typing import Any

from bson import ObjectId
from fastapi import Request, HTTPException, status

from app.core.db import user_collection
from app.core.security import decode_access_token


def unauthorized(message: str = "Authentication required"):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "success": False,
            "message": message,
            "error": {
                "code": "AUTHENTICATION_REQUIRED",
                "message": message,
            },
        },
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(request: Request) -> dict[str, Any]:
    """
    Authentication:
    1. Extract JWT from Authorization header or cookie.
    2. Decode and validate JWT.
    3. Retrieve user from MongoDB.
    4. Return authenticated user.
    """

    # Extract token from Authorization header
    authorization = request.headers.get("Authorization")
    token = None

    if authorization:
        scheme, separator, credentials = authorization.partition(" ")

        if separator and scheme.lower() == "bearer":
            token = credentials.strip()

    # Fallback to HTTP-only cookie
    if not token:
        token = request.cookies.get("access_token")

    if not token:
        raise unauthorized()

    # Decode JWT
    try:
        payload = decode_access_token(token)
    except Exception:
        raise unauthorized("Invalid or expired token")

    user_id = payload.get("user_id")

    if not user_id or not ObjectId.is_valid(user_id):
        raise unauthorized("Invalid token payload")

    # Retrieve user from MongoDB
    user = await user_collection.find_one(
        {"_id": ObjectId(user_id)}
    )

    if not user:
        raise unauthorized("User not found")

    return {
        "id": str(user["_id"]),
        "name": user.get("name"),
        "email": user.get("email"),
        "username": user.get("username"),
        "role": user.get("role"),
        "is_active": user.get("is_active", False),
        "is_email_verified": user.get("is_email_verified", False),
    }


async def require_active_user(
    current_user: dict = __import__("fastapi").Depends(get_current_user),
):
    """
    Authentication + active account validation.
    """
    # print("AUTH DEPENDENCY EXECUTED")


    if not current_user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is inactive",
        )

    return current_user


def require_roles(*allowed_roles: str):
    """
    Authorization:
    Allow only users whose role is in allowed_roles.
    """

    async def role_checker(
        current_user: dict = __import__("fastapi").Depends(require_active_user),
    ):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this resource",
            )

        return current_user

    return role_checker
