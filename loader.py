from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

print("Loading PDF...")

loader = PyPDFLoader("Hands_On_Machine_Learning_with_Scikit_Learn,_Keras,_and_Tensorflow.pdf")
docs = loader.load()

print("Pages:", len(docs))

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=30
)

chunks = splitter.split_documents(docs)

print("Chunks:", len(chunks))

# ✅ FIXED EMBEDDINGS (STABLE)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create vector DB
db = FAISS.from_documents(chunks, embeddings)

# Save
db.save_local("my_db")

print("✅ Vector DB created successfully!")
