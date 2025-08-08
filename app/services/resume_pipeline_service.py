from .ocr_service import extract_text_from_image
from .parsing_service import order_resume_into_dictionary_LLM
from .chunking_service import chunk_resume
from .embedding_service import embed_texts
from .vectorstore_service import add_to_vectorstore
from .resume_service import save_resume_image

def process_resume_pipeline(image_path: str, resume_image_url: str = "") -> str:
    raw_text = extract_text_from_image(image_path)
    resume_dict = order_resume_into_dictionary_LLM(raw_text)
    chunks, resume_id = chunk_resume(resume_dict, resume_image_url)
    
    save_resume_image(resume_id, image_path)
    
    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    
    embeddings = embed_texts(texts)
    add_to_vectorstore(texts, ids, metadatas, embeddings)

    return resume_id