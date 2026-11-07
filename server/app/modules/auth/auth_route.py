from fastapi import APIRouter, status, Response, Request
from app.shared.schemas.api_response import APIResponse
from app.modules.user.user_schema import UserResponse, UserCreate
from app.modules.auth.auth_schema import UserLogin, TokenResponse
from app.modules.auth.auth_controller import register_user_controller, login_user_controller
from app.core.config import settings
from app.core.success_res import success_res

 
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login", response_model=APIResponse[TokenResponse], status_code=status.HTTP_200_OK)
async def login_user(res: Response, data: UserLogin):
    token = await login_user_controller(data)
    res.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        samesite="lax",
        path="/",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return success_res(token, "Login Successfully")


@router.post("/logout", response_model=APIResponse[None], status_code=status.HTTP_200_OK)
async def logout_user(res: Response):
    res.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        samesite="lax",
    )
    return success_res(None, "Logout Successfully")


@router.post("/register", response_model=APIResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def register_user(data: UserCreate):
    await register_user_controller(data)

    return success_res(None, "User Created Successfully")
