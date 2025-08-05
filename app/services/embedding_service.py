from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

def embed_texts(texts):
    return model.encode(texts).tolist()

def embed_query(query: str):
    return model.encode([query]).tolist()
