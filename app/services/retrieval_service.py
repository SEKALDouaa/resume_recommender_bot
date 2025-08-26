from app.services.embedding_service import embed_query
from app.services.vectorstore_service import query_vectorstore
from langchain.schema import Document
import logging

# Optional: Configure logging if not done elsewhere
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def retrieve_documents(query: str, k=5):
    query_embedding = embed_query(query)
    raw_results = query_vectorstore(query_embedding, k)

    # Group chunks by resume_id
    grouped = {}
    for text, metadata in raw_results:
        resume_id = metadata.get("resume_id", "unknown_resume")
        if resume_id != "unknown_resume":
            metadata["image_url"] = f"http://localhost:5000/simple_resume/resume_image/{resume_id}"
        grouped.setdefault(resume_id, []).append(text)

    grouped_docs = []
    logger.debug(f"Number of grouped resumes: {len(grouped)}")

    for resume_id, texts in grouped.items():
        full_text = "\n\n---\n\n".join(texts)
        logger.debug(f"Resume ID: {resume_id}, Number of chunks: {len(texts)}")
        preview = full_text[:300].replace("\n", " ")
        logger.debug(f"Preview of concatenated text: {preview}...")
        grouped_docs.append(
            Document(
                page_content=full_text,
                metadata={"resume_id": resume_id, "num_chunks": len(texts)}
            )
        )

    # ✅ Sort documents by number of chunks (descending)
    grouped_docs.sort(key=lambda d: d.metadata["num_chunks"], reverse=True)

    return grouped_docs
