from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool

load_dotenv()

parser = StrOutputParser()


@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."

@tool
def get_temperature(location: str) -> str:
    """Get the temperature at a location."""
    return f"The temperature in {location} is 39°C."

tools_registry = {
    "get_weather": get_weather,
    "get_temperature": get_temperature
}

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
).bind_tools([get_weather, get_temperature])


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a backend engineering teacher."
    ),
    (
        "human",
        "Explain {topic} in simple terms and in 5 line."
    )
])


# output of prompt becomes input of model. output of model becomes input of parser

# chain = prompt | model | parser

messages = [{"role": "user", "content": "what's the weather in Delhi and temperature in Mumbai?"}]

while True:

    response = model.invoke(messages)
    messages.append(response)

    if response.tool_calls:
        for tool_call in response.tool_calls:
            print("function called: ", tool_call["name"])

            tool = tools_registry[tool_call["name"]]
            tool_result = tool.invoke(tool_call)
            messages.append(tool_result)
        continue
    else:
        print("AI: ", parser.invoke(response.content[0]["text"]))
        break


# for chunk in chain.stream({"topic": "Kafka"}):
#     print(chunk, end='|', flush=True)

# response = chain.invoke()


# print(response.content)

# print('type of response is ', type(response))