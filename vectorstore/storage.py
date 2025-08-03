import chromadb
from chromadb.config import Settings

chroma_client = chromadb.Client(Settings(
    chroma_db_impl = "duckdb+parquet",
    persistence_directory="chroma_db"
))

collection = chroma_client.get_or_create_collection(name='resumes')

texts = [chunk["text"] for chunk in resume_to_embed]
ids = [chunk["id"] for chunk in resume_to_embed]
metadatas = [chunk["metadata"] for chunk in resume_to_embed]

embeddings = model.encode(texts).tolist()

collection.add(documents=texts, metadata= metadatas,ids= ids, embeddings= embeddings)
chroma_client.persist()

query = "Business analyst with reporting experience"
query = model.encode([query]).tolist()

results = collection.query(query_embedding = query_embedding, n_results= 5)
for doc, meta in zip(results[["documents"][0]], results[["metadata"][0]]):
    print("Match:", doc)
    print("Metadata:", meta)
    print("-----")