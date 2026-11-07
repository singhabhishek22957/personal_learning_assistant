from app.core.llm import llm
from app.modules.chat.graph.state import ChatState


async def chat_node(state: ChatState):

    response = await llm.ainvoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }