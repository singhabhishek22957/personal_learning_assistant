from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from app.modules.chat.graph.state import ChatState
from app.modules.chat.graph.nodes import chat_node


def build_chat_graph():

    # Create graph
    graph_builder = StateGraph(ChatState)

    # Register nodes
    graph_builder.add_node("chat", chat_node)

    # Define workflow
    graph_builder.add_edge(START, "chat")
    graph_builder.add_edge("chat", END)

    # In-memory checkpoint
    checkpointer = InMemorySaver()

    # Compile graph
    graph = graph_builder.compile(
        checkpointer=checkpointer
    )

    return graph


chat_graph = build_chat_graph()