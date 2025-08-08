from app.services.embedding_service import embed_query
from app.services.vectorstore_service import query_vectorstore
from langchain.schema import Document

def retrieve_documents(query: str, k=5):
    query_embedding = embed_query(query)
    raw_results = query_vectorstore(query_embedding, k)

    docs = []
    for text, metadata in raw_results:
        # Add image URL if resume_id is present in metadata
        if "resume_id" in metadata:
            metadata["image_url"] = f"/resume_image/{metadata['resume_id']}"
        docs.append(Document(page_content=text, metadata=metadata))

    return docs
