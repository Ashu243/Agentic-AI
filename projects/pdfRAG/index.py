from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS




load_dotenv()

loader = PyPDFLoader("sample.pdf")

documents = loader.lazy_load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " ", ""]
)

chunks = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

# texts = [chunk.page_content for chunk in chunks]

# vector = embeddings.embed_documents(texts)

vectorstore = FAISS.from_documents(chunks, embeddings)


vectorstore.save_local("faiss_index")
print("FAISS index created and saved!")
