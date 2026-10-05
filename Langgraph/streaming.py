from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.config import get_stream_writer


class State(TypedDict):
    topic: str
    joke: str


def generate_joke(state: State):
    writer = get_stream_writer()

    writer({"status": "Starting..."})
    writer({"status": "Thinking about the topic..."})
    writer({"status": "Creating the setup..."})
    writer({"status": "Adding the punchline..."})
    writer({"status": "Almost done..."})

    return {
        "joke": f"Why did the {state['topic']} go to school? "
                "Because it wanted to get a sundae education!"
    }
graph = (
    StateGraph(State)
    .add_node(generate_joke)
    .add_edge(START, "generate_joke")
    .add_edge("generate_joke", END)
    .compile()
)

for chunk in graph.stream(
    {"topic": "ice cream"},
    stream_mode=["updates", "custom"],
    version="v2",
):
    if chunk["type"] == "updates":
        for node_name, state in chunk["data"].items():
            print(f"Node {node_name} updated: {state}")
    elif chunk["type"] == "custom":
        print(f"Status: {chunk['data']['status']}")