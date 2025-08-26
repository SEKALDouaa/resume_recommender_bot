from app.services.llm_service import llm
from app.services.retrieval_service import retrieve_documents
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.schema import BaseRetriever

class CustomRetriever(BaseRetriever):
    # Wraps our retrieval logic for LangChain
    def get_relevant_documents(self, query: str):
        return retrieve_documents(query)


# Prompt: structured and ranking-focused
prompt_template = """
You are a helpful assistant that answers questions about resumes.

The user asked: {question}

You are given excerpts (chunks) from resumes. 
Only use the information explicitly stated in these chunks. 
If some details (e.g., job title, skills, company) are missing from the provided chunks, 
DO NOT make them up — just say "Not available in the provided context".

Your task:
1. State the total number of resumes matched.  
2. Rank the resumes from most relevant to least relevant (best → worst).  
3. For each ranked resume, summarize key info (Job Title, Experience, Skills, Company).  
4. Always include the `resume_id` (if available in metadata) so it can be linked to the resume image.

Excerpts:
{context}

Answer:
"""

# Instantiate retriever and chain
retriever = CustomRetriever()
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    return_source_documents=True,
    chain_type_kwargs={
        "prompt": PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
    }
)


def generate_rag_response(query: str):
    # Get both the LLM’s answer and the raw source docs
    result = qa_chain.invoke({"query": query})

    answer_text = result["result"]
    source_docs = result.get("source_documents", [])

    # Build a structured mapping of resumes
    ranked_resumes = []
    for idx, doc in enumerate(source_docs, start=1):
        resume_entry = {
            "rank": idx,
            "resume_id": doc.metadata.get("resume_id", f"resume_{idx}"),
            "image_url": doc.metadata.get("image_url", None),
            "text_excerpt": doc.page_content[:300]  # optional preview
        }
        ranked_resumes.append(resume_entry)

    return {
        "answer": answer_text,        # LLM summary & ranking
        "ranked_resumes": ranked_resumes  # ordered list with IDs + image links
    }
