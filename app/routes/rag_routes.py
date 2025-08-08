from flask import Blueprint, request, jsonify
from ..services.rag_service import generate_rag_response  # extract the RAG logic to qa_service.py

qa_bp = Blueprint("qa_bp", __name__)

@qa_bp.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    query = data['query']

    try:
        answer = generate_rag_response(query)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
