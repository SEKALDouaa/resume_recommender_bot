import json
import time
from app.services.rag_service import generate_rag_response

# Path to your dataset
EVALUATION_FILE = "app/evaluation/evaluation_dataset.json"

# Delay between queries (in seconds) to avoid rate limit issues
DELAY_BETWEEN_QUERIES = 5

def evaluate_rag_item(item):
    query = item["query"]
    correct_resumes = set(item["correct_resumes"])
    required_keywords = set(k.lower() for k in item.get("required_keywords", []))
    optional_keywords = set(k.lower() for k in item.get("optional_keywords", []))

    # Call RAG pipeline
    rag_output = generate_rag_response(query)

    ranked_resumes = rag_output["ranked_resumes"]
    answer_text = rag_output["answer"].lower()

    # Compute metrics
    retrieved_ids = [r["resume_id"] for r in ranked_resumes]

    # Recall@k (here k = number of correct resumes)
    recall = len(correct_resumes.intersection(retrieved_ids)) / len(correct_resumes) if correct_resumes else 0

    # Precision@k (fraction of retrieved that are correct)
    precision = len(correct_resumes.intersection(retrieved_ids)) / len(retrieved_ids) if retrieved_ids else 0

    # Required keyword coverage
    req_kw_covered = sum(1 for kw in required_keywords if kw in answer_text) / len(required_keywords) if required_keywords else 0

    # Optional keyword coverage
    opt_kw_covered = sum(1 for kw in optional_keywords if kw in answer_text) / len(optional_keywords) if optional_keywords else 0

    return {
        "query": query,
        "recall": recall,
        "precision": precision,
        "required_keyword_coverage": req_kw_covered,
        "optional_keyword_coverage": opt_kw_covered,
        "retrieved_ids": retrieved_ids,
        "answer": answer_text
    }

def main():
    with open(EVALUATION_FILE, "r", encoding="utf-8") as f:
        evaluation_dataset = json.load(f)

    results = []
    for item in evaluation_dataset:
        print(f"Evaluating query: {item['query']}")
        result = evaluate_rag_item(item)
        results.append(result)
        print(f"  Recall: {result['recall']:.2f}, Precision: {result['precision']:.2f}, ReqKW: {result['required_keyword_coverage']:.2f}, OptKW: {result['optional_keyword_coverage']:.2f}")
        time.sleep(DELAY_BETWEEN_QUERIES)

    # Save results
    with open("rag_evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("Evaluation complete. Results saved to rag_evaluation_results.json")

if __name__ == "__main__":
    main()
