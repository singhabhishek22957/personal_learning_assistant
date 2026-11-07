from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.dependencies.auth import require_active_user
from app.modules.chat.chat_schema import ChatRequest
from app.modules.chat.chat_service import stream_chat_response


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    dependencies=[Depends(require_active_user)]
)


@router.post("/conversations/{conversation_id}/messages/stream")
async def send_message(
    conversation_id: UUID,
    payload: ChatRequest,
    user: dict = Depends(require_active_user),
):

    return StreamingResponse(
        stream_chat_response(
            user_id=user["id"],
            conversation_id=str(conversation_id),
            message=payload.message,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )