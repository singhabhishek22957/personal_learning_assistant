import json
import logging

from langchain_core.messages import HumanMessage

from app.modules.chat.graph.builder import chat_graph

logger = logging.getLogger(__name__)


def get_thread_id(user_id: str, conversation_id: str) -> str:
    # Isolate conversations by user
    return f"{user_id}:{conversation_id}"


async def stream_chat_response(
    user_id: str,
    conversation_id: str,
    message: str,
):
    thread_id = get_thread_id(user_id, conversation_id)

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:
        async for chunk, metadata in chat_graph.astream(
            {
                "messages": [
                    HumanMessage(content=message)
                ]
            },
            config=config,
            stream_mode="messages",
        ):

            # Only stream output from our chat node
            if metadata.get("langgraph_node") != "chat":
                continue

            content = chunk.content

            if isinstance(content, str) and content:
                yield f"event: token\ndata: {json.dumps({'content': content})}\n\n"

            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text = block.get("text", "")
                        if text:
                            yield f"event: token\ndata: {json.dumps({'content': text})}\n\n"

        yield "event: done\ndata: {}\n\n"

    except Exception:
        logger.exception(
            "Chat generation failed | user_id=%s | conversation_id=%s",
            user_id,
            conversation_id,
        )

        yield (
            "event: error\n"
            'data: {"message":"Unable to generate response"}\n\n'
        )