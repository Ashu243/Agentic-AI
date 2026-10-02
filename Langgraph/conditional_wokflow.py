from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from pydantic import BaseModel, Field


load_dotenv()

class State(TypedDict):
    review: str
    feedback: str
    reply: str

class Feedback(BaseModel):
    feedback: str = Field(description="positive or negative")
    urgency: int = Field(description='score from 1 to 10 on the basis of urgency in review')

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)

model_with_Structured_output = model.with_structured_output(Feedback)


graph = StateGraph(State)

def get_feedback(state: State):
    review = state['review']

    ans = model_with_Structured_output.invoke(review)


    return {
        'feedback': ans.feedback
    }

def get_positive_reply(state: State):
    review = state['review']

    prompt = f"""
You are a customer support representative replying to a customer who left a positive review.

Write a short, warm, and natural reply to the customer.

Customer review:
{review}
"""

    ans = model.invoke(prompt).content[0]['text']

    return {
        'reply': ans
    }


def get_negative_reply(state: State):
    review = state['review']

    prompt = f"""
You are a customer support representative replying to a customer who left a negative review.

Write a short and natural reply to the customer.

Customer review:
{review}
"""

    ans = model.invoke(prompt).content[0]['text']

    return {
        'reply': ans
    }

def check_feedback(state: State):
    feedback = state['feedback']

    if feedback == 'positive':
        return 'positive_reply'
    else:
        return 'negative_reply'



graph.add_node('feedback', get_feedback)
graph.add_node('positive_reply', get_positive_reply)
graph.add_node('negative_reply', get_negative_reply)


graph.add_edge(START, 'feedback')
graph.add_conditional_edges('feedback', check_feedback)


graph.add_edge('positive_reply', END)
graph.add_edge('negative_reply', END)

workflow = graph.compile()

initial_state = {'review': 'This smartphone is totally worth it! Do buy it.'}

final_state = workflow.invoke(initial_state)

print(final_state['reply'])



