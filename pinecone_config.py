from pinecone import Pinecone
import os

def init_pinecone():
    pinecone_api_key = os.getenv('PINECONE_API_KEY')
    pc = Pinecone(api_key = pinecone_api_key)
# Create or connect to an existing Pinecone index
    index_name = "book-embeddings"
    index = pc.Index(index_name)
    return index