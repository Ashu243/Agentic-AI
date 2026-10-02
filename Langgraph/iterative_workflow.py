from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from pydantic import BaseModel, Field

load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)

class Score(BaseModel):
    score: int = Field(description="Score from 1 to 10 based on the explanation")

model_with_Structured_Output = model.with_structured_output(Score)


class State(TypedDict):
    topic: str
    explanation: str
    score: int
    improve: str

graph = StateGraph(State)


# define functions
def gen_explanation(State: State):
    topic = State['topic']
    prompt = f"Generate a very short explanation on {topic}. Do some mistakes in it"
    ans = model.invoke(prompt).content[0]['text']

    return {
        'explanation': ans,
        'improve': ans
    }

def imp_explanation(State: State):
    improve = State['improve']

    prompt = f'improve and rewrite this explanation: {improve}'
    ans = model.invoke(prompt).content[0]['text']

    return {
        'improve': ans
    }
    
def score_explanation(State: State):
    explanation = State['improve']
    topic = State['topic']
    prompt = f"check the given explanation and generate a score out of 10 based on the explanation. Topic: {topic} Explantion: {explanation}"

    ans = model_with_Structured_Output.invoke(prompt)
    return {
        'score': ans.score
    }

def check_explanation(State: State):
    score = State['score']

    if score > 7:
        return "Done"
    else:
        return "improve"


# create nodes
graph.add_node('generate_explanation', gen_explanation)
graph.add_node('improve_explanation', imp_explanation)
graph.add_node('score_explanation', score_explanation)
graph.add_node('check_explantion', check_explanation)

# add edges
graph.add_edge(START, 'generate_explanation')
graph.add_edge('generate_explanation', 'score_explanation')
graph.add_conditional_edges('score_explanation', check_explanation, {"Done": END, "improve": "improve_explanation"})
graph.add_edge('improve_explanation', 'score_explanation')

# compile the graph
workflow = graph.compile()

# execute the Graph
initial_state = {'topic': "langgraph"}
final_state = workflow.invoke(initial_state)


print(final_state['explanation'], '\n')
print("final score: ",final_state['score'])
print(final_state['improve'])
