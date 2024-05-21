import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
from pinecone import Pinecone, ServerlessSpec
import os
import itertools
from pinecone_config import init_pinecone

# Replace 'your_file_path.csv' with the path to your CSV file
df = pd.read_csv('df_chunk_14.csv', low_memory=False)

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

index = init_pinecone()
# pinecone_api_key = os.getenv('PINECONE_API_KEY')
# pc = Pinecone(api_key = pinecone_api_key)

# # Create or connect to an existing Pinecone index
# index_name = "book-embeddings"
# index = pc.Index(index_name)

#correct code

def generate_embedding(text):
    if pd.isna(text):
        return None  # Return None or an appropriate value for NaN entries
    text = str(text)  # Ensure the input is a string
    inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(1).squeeze().tolist()
    return embeddings

print("Generating embeddings...")

# Apply the function to the 'Summary' column
df["title_embedding"] = df["book_title"].apply(generate_embedding)
#df["summary_embedding"] = df["Summary"].apply(generate_embedding)

print("Adding data to Pinecone...")

def upload_batch_to_pinecone(batch_df):
    items_to_upload = []
    for _, row in batch_df.iterrows():
        if row['title_embedding'] is not None:  # Check if embedding is not None
            items_to_upload.append(
                (str(row['isbn']), row['title_embedding'], {
                    "rating": row['rating'],
                    "book_title": row['book_title'],
                    "book_author": row['book_author'],
                    "year_of_publication": str(row['year_of_publication']),
                    "publisher": row['publisher'],
                    "img_l": row['img_l'],
                    "Summary": row['Summary'],
                    "Language": row['Language'],
                    "Category": row['Category']
                })
            )
    #Upload the data to Pinecone
    #index.upsert(vectors=items_to_upload)
    # Upsert data with 100 vectors per upsert request
    for ids_vectors_chunk in chunks(items_to_upload, batch_size=100):
        index.upsert(vectors=ids_vectors_chunk)
        print("Chunk uploaded....")

def chunks(iterable, batch_size=100):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))

upload_batch_to_pinecone(df)


print("All data has been uploaded to Pinecone.")


