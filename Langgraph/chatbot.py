from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END, add_messages
from typing import TypedDict, Annotated
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)

@tool
def get_news():
    """
    Get the latest cricket news.
    """
    return """🇮🇳 India win Asian Games gold — India defeated Pakistan by 19 runs in the men's T20 cricket final in Japan, successfully defending their Asian Games title. The Indian Express
🏏 Shai Hope destroys India’s bowling — West Indies captain Shai Hope smashed an unbeaten 162 as West Indies chased down India’s 351/5 and won the 3rd ODI by 5 wickets. NDTV Sports
🇮🇳 India win the ODI series 2–1 — Despite losing the final ODI, India had already secured the series with victories in the first two matches. NDTV Sports
🏆 Rest of India win Irani Cup — Rest of India defeated Ranji champions Jammu & Kashmir by 167 runs. Mukesh Kumar and Akash Deep took nine wickets between them. The Times of India
⚠️ New ICC time-wasting rule — Batters can now cost their team 5 penalty runs for repeatedly failing to be ready for a delivery. The penalty begins from the third offence."
"""

def getresponse(state: State):

    response = model_with_tools.invoke(state["messages"])

    print(response)

    return {
        "messages": [response]
    }



tools = [get_news]
model_with_tools = model.bind_tools(tools)

graph = StateGraph(State)

tool_node = ToolNode(tools)

graph.add_node('chat', getresponse)
graph.add_node('tools', tool_node)

graph.add_edge(START, 'chat')
graph.add_conditional_edges('chat', tools_condition)
graph.add_edge('tools', 'chat')

checkpointer = InMemorySaver()
workflow = graph.compile(checkpointer=checkpointer)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

while True:
    user_query = input("\nUser: ")

    if user_query.lower() == 'exit':
        break

    initial_state = {'messages': [
        HumanMessage(content=user_query)
    ]}
    final_state = workflow.invoke(initial_state, config=config)

    print(final_state["messages"][-1].content[0]['text'])