import os
import uuid
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from chromadb import PersistentClient

class RetrievalAgent:
    def __init__(self, collection_name="docs"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = PersistentClient(path=".chroma_db")  # ✅ Updated
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_documents(self, chunks, metadata_list=None):
        embeddings = self.model.encode(chunks).tolist()
        ids = [str(uuid.uuid4()) for _ in chunks]
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadata_list or [{"source": "manual_test"} for _ in chunks],
            ids=ids
        )

    def retrieve(self, query, top_k=3):
        embedding = self.model.encode([query])[0].tolist()
        results = self.collection.query(query_embeddings=[embedding], n_results=top_k)
        return results["documents"][0]  # top_k matching chunks

    def clear(self):
        self.client.delete_collection(name=self.collection.name)
        self.collection = self.client.get_or_create_collection(name=self.collection.name)

