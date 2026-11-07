import os

from langchain_ollama import ChatOllama

llm = ChatOllama(
    model=os.getenv("OLLAMA_MODEL", "qwen3:4b"),
    base_url=os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    ),
    temperature=0.3,
)