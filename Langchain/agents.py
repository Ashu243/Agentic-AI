from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv

from langchain_core.output_parsers import StrOutputParser

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

messages = [{
    "role": "user",
    "content": "what's the weather of Gurugram and temperature of Mumbai?"
}]

agent = create_agent(
    model="google_genai:gemini-3.5-flash-lite",
    tools=[get_weather, get_temperature],
    )


result = agent.invoke({"messages": messages})

for message in result["messages"]:
    print(type(message).__name__)
    print(message)
    print("----------------")