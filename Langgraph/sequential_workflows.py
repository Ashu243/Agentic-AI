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
    improved: str


# create a Graph
graph = StateGraph(State)


# define functions
def gen_explanation(State: State):
    topic = State['topic']
    prompt = f"Generate a simple and short explanation on {topic}"
    ans = model.invoke(prompt).content[0]['text']

    return {
        'explanation': ans
    }

def imp_explanation(State: State):
    explanation = State['explanation']

    prompt = f'improve this explanation: {explanation}'
    ans = model.invoke(prompt).content[0]['text']

    return {
        'improved': ans
    }
    

# create nodes
graph.add_node('generate_explanation', gen_explanation)
graph.add_node('improve_explanation', imp_explanation)

# add edges
graph.add_edge(START, 'generate_explanation')
graph.add_edge('generate_explanation', 'improve_explanation')
graph.add_edge('improve_explanation', END)

# compile the graph
workflow = graph.compile()

# execute the Graph
initial_state = {'topic': "langgraph"}
final_state = workflow.invoke(initial_state)

print("explanation:", final_state['explanation'], '\n')
print('---------------------')
print("improved:", final_state['improved'], '\n')
