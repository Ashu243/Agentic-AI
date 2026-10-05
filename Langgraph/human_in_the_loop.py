from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


class State(TypedDict):
    email: str
    status: str


def prepare_email(state: State):

    email = """Subject: Unable to Attend Class

Dear Professor,

I won't be able to attend class tomorrow due to personal reasons.
I apologize for the inconvenience.

Regards,
Ashu
"""

    return {"email": email}


def approve_email(state: State):

    approval = interrupt(
        f"\nEmail to send:\n\n{state['email']}\n"
        "\nDo you want to send this email?"
    )

    if approval.lower() == "yes":
        return {"status": "approved"}

    return {"status": "cancelled"}


def send_email(state: State):

    if state["status"] == "approved":
        print("\n📧 Email sent!")
        print(state["email"])
        return {"status": "sent"}

    print("\n❌ Email cancelled.")
    return {"status": "cancelled"}



graph = StateGraph(State)

graph.add_node("prepare_email", prepare_email)
graph.add_node("approve_email", approve_email)
graph.add_node("send_email", send_email)

graph.add_edge(START, "prepare_email")
graph.add_edge("prepare_email", "approve_email")
graph.add_edge("approve_email", "send_email")
graph.add_edge("send_email", END)

checkpointer = InMemorySaver()

workflow = graph.compile(
    checkpointer=checkpointer
)



config = {
    "configurable": {
        "thread_id": "email-1"
    }
}

result = workflow.invoke(
    {},
    config=config
)

print("\nGraph paused.")


user_input = input("\nSend the email? (yes/no): ")

# Resume the graph
result = workflow.invoke(
    Command(resume=user_input), # the user_input becomes the result of interrupt
    config=config
)

print("\nFinal state:")
print(result)