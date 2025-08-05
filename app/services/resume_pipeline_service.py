from services.ocr_service import extract_text_from_image
from services.parsing_service import order_resume_into_dictionary
from services.chunking_service import chunk_resume
from services.embedding_service import embed_texts
from services.vectorstore_service import add_to_vectorstore

def process_resume_pipeline(image_path: str, resume_image_url: str = "") -> str:
    raw_text = extract_text_from_image(image_path)
    resume_dict = order_resume_into_dictionary(raw_text)
    chunks, resume_id = chunk_resume(resume_dict, resume_image_url=resume_image_url)
    
    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    
    embeddings = embed_texts(texts)
    add_to_vectorstore(texts, ids, metadatas, embeddings)

    return resume_id