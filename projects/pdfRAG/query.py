from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

user_query = "What are lists in Python?"

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)



context = ""

def format_documents(documents):
    context = ""

    for i, doc in enumerate(documents):
        context += f"""
--- Context {i + 1} ---
{doc.page_content}

Source: {doc.metadata.get("source")}
Page: {doc.metadata.get("page")}
"""

    return context

# 6. Create prompt
prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant.

Answer the question using ONLY the provided context.

If the context does not contain enough information,
say that you don't have enough information.

Context:
{context}

user_query:
{user_query}

Keep the answer concise and simple.
""")

# 7. Send prompt to Gemini
model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)

chain = (
    # we need to create both values from that one input.
    {
        "context": retriever | format_documents, # means: Send the user's question to the retriever and use its output as context.
        "user_query": RunnablePassthrough() # means: "Don't change the input. Just pass it through." receives user_query -> returns user_query
    }
    | prompt
    | model
)

response = chain.invoke(user_query)

print("Prompt: ", prompt)

# 8. Print answer
print(response.content)




#  The first part of the chain produces the result something like this:
#{
#     "context": "...formatted documents...",
#     "user_query": "What are lists in Python?"
# }
# This concept is called -> RunnableParallel. cause first part of the chain is going in two branches
# we can also write that as 
# parallel = RunnableParallel(
#     context=retriever | format_documents,
#     question=RunnablePassthrough()
# ) --> then parallel.invoke("what are lists in python")



# RunnablePassthrough.assign() — add something to existing data
# we could have also done like Runnablepassthrough.assign(context=retriever | format_docs)

# RunnableSequence - when we write: "retriever | format_docs | prompt | model" this is runnablesequence