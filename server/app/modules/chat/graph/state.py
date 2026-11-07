from langgraph.graph import MessagesState


class ChatState(MessagesState):
    """
    State for the chat graph.

    MessagesState already provides:
    - messages
    - add_messages reducer
    """
    pass