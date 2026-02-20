import os
import uuid
from typing import List
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Database Configuration
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../chroma_db"))
COLLECTION_NAME = "documents"
MODEL_NAME = "all-MiniLM-L6-v2"

# 1. Initialize persistent ChromaDB client
client = chromadb.PersistentClient(path=DB_PATH)

# 2. Load embedding model
# Note: Initial load might take a few seconds to download/init the model
model = SentenceTransformer(MODEL_NAME)

# 3. Create or load collection
collection = client.get_or_create_collection(name=COLLECTION_NAME)

def store_chunks(chunks: List[str], filename: str):
    """
    Converts text chunks into embeddings and stores them in ChromaDB.
    """
    if not chunks:
        return
    
    # Generate embeddings for all chunks
    embeddings = model.encode(chunks).tolist()
    
    # Generate unique IDs for each chunk
    ids = [str(uuid.uuid4()) for _ in chunks]
    
    # Create metadata for each chunk
    metadatas = [{"filename": filename} for _ in chunks]
    
    # Store in ChromaDB
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )
    print(f"Stored {len(chunks)} chunks from {filename} in Vector DB.")

def search_chunks(query: str, n_results: int = 3):
    """
    Searches for the most relevant chunks in ChromaDB based on a query.
    """
    # Convert query into embedding
    query_embedding = model.encode([query]).tolist()
    
    # Perform search
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    
    # Return documents (the actual text chunks)
    # results['documents'] is a list of lists, we take the first sub-list
    return results.get('documents', [[]])[0]
