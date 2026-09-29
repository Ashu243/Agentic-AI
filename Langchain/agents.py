from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv

from langchain_core.output_parsers import StrOutputParser
from langgraph.checkpoint.sqlite import SqliteSaver

parser = StrOutputParser()

load_dotenv()


@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."

@tool
def get_temperature(location: str) -> str:
    """Get the temperature at a location."""
    return f"The temperature in {location} is 39°C."

with SqliteSaver.from_conn_string("agent.db") as checkpointer:

    agent = create_agent(
        model="google_genai:gemini-3.5-flash-lite",
        tools=[get_weather, get_temperature],
        checkpointer=checkpointer,
    )

    config = {
        "configurable": {
            "thread_id": "ashu-chat-1"
        }
    }

    while True:

        user_input = input("You: ")

        if user_input == "exit":
            break

        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            },
            config=config
        )

        print("AI:", result["messages"][-1].content[0]["text"])