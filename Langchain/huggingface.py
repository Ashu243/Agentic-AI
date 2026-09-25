from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv

load_dotenv()

# model name and task type
llm = HuggingFaceEndpoint(
    repo_id="ibm-granite/granite-4.2-30b",
    task='text-generation'
)

model = ChatHuggingFace(llm=llm)

result = model.invoke('what is the capital of japan?')

print(result.content)

