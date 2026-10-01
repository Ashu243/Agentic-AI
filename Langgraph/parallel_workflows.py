from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict


load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)

class State(TypedDict):
    topic: str
    explanation: str
    advantages: str
    use_cases: str
    summary: str

def gen_explanation(State: State):
    topic = State['topic']
    prompt = f"generate a simple and short explanation on {topic}"

    ans = model.invoke(prompt).content[0]['text']

    return {
        'explanation': ans
    }


def gen_advantages(State: State):
    topic = State['topic']
    prompt = f"generate a simple and short advantages of {topic}"

    ans = model.invoke(prompt).content[0]['text']

    return {
        'advantages': ans
    }

def gen_use_cases(State: State):
    topic = State['topic']
    prompt = f"generate a simple and short use cases of {topic}"

    ans = model.invoke(prompt).content[0]['text']

    return {
        'use_cases': ans
    }
def gen_summary(State: State):
    explanation = State['explanation']
    advantages = State['advantages']
    use_cases = State['use_cases']

    prompt = f"Generate the final summary, here is the explanation: {explanation}, advantages: {advantages}, use_cases: {use_cases}"
    ans = model.invoke(prompt).content[0]['text']

    return {
        'summary': ans
    }

graph = StateGraph(State)

graph.add_node('explanation', gen_explanation)
graph.add_node('advantages', gen_advantages)
graph.add_node('use_cases', gen_use_cases)
graph.add_node('summary', gen_summary)


graph.add_edge(START, 'explanation')
graph.add_edge(START, 'advantages')
graph.add_edge(START, 'use_cases')

graph.add_edge('explanation', 'summary')
graph.add_edge('advantages', 'summary')
graph.add_edge('use_cases', 'summary')

graph.add_edge('summary', END)

workflow = graph.compile()


initial_state = {'topic': "Redis"}

final_state = workflow.invoke(initial_state)
print(final_state['summary'])

