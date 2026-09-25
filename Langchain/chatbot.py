from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from pydantic import BaseModel, Field




load_dotenv()


# schema for ai responses
class SupportRequest(BaseModel):

    category: str = Field(
        description="The category of the user's issue"
    )

    urgency: str = Field(
        description="The urgency level: low, medium, or high"
    )

    confidence: float = Field(
        description="The model's confidence between 0 and 1"
    )

parser = StrOutputParser()

@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."

model = ChatGoogleGenerativeAI(model="gemini-3.6-flash").with_structured_output(SupportRequest)


chain = model


# query can be like "My payment failed and money was deducted from my account."
while (True):
    user_input = input('You: ')
    if user_input == 'exit':
        break
    result = chain.invoke(user_input)
    print("AI: ", result)