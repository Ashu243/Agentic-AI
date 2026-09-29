from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()


documents = [
    Document(
        page_content="Redis is an in-memory data store commonly used for caching.",
        metadata={"topic": "redis"}
    ),
    Document(
        page_content="Redis can also be used for queues, pub/sub, and distributed locks.",
        metadata={"topic": "redis"}
    ),
    Document(
        page_content="PostgreSQL is a relational database that uses SQL.",
        metadata={"topic": "postgresql"}
    ),
    Document(
        page_content="Docker packages applications and their dependencies into containers.",
        metadata={"topic": "docker"}
    ),
]


embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

# takes documents and embedding function to use and stores the document and vector embedding in vector_store
vector_store = FAISS.from_documents(
    documents,
    embeddings
)


retriever = vector_store.as_retriever(
    search_kwargs={"k": 2, "score_threshold": 0.8}
)


docs = retriever.invoke(
    "What is Redis used for?"
)


for doc in docs:
    print("Content:", doc.page_content)
    print("Metadata:", doc.metadata)