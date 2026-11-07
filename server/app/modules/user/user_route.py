from fastapi import APIRouter , status , Request , Depends
from app.shared.schemas.api_response import APIResponse
from app.modules.user.user_schema import UserResponse
from app.core.success_res import success_res
from app.dependencies.auth import require_active_user


router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies = [Depends(require_active_user)]
)






@router.get("/me", response_model=APIResponse[UserResponse] , status_code=status.HTTP_200_OK)
async def get_current_user(req:Request, user = Depends(require_active_user)):
    user =user
    return success_res(user, "User Fetched Successfully")


@router.get("/")
async def user_home():
    return { "message":"testing user home route only access by authenticated person"}