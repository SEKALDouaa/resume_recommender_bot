from app.services.llm_service import llm
from app.services.retrieval_service import retrieve_documents
from langchain.chains import RetrievalQA
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.schema import BaseRetriever

class CustomRetriever(BaseRetriever): #we "trick" langchain into using our method by wrapping our method in a class that implements the expected interface using our method
    def get_relevant_documents(self, query: str):
        return retrieve_documents(query)

# Instantiate retriever and chain
retriever = CustomRetriever()
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"  # Or "refine", "map_reduce"
)

def generate_rag_response(query: str) -> str:
    return qa_chain.run(query)
