from flask import Blueprint, request, jsonify
from services.resume_pipeline_service import process_resume_pipeline  # put the full pipeline in resume_pipeline.py

resume_bp = Blueprint("resume", __name__)

@resume_bp.route("/process-resume", methods=["POST"])
def process_resume():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']
    image_path = f"/tmp/{image.filename}"
    image.save(image_path)

    image_url = request.form.get("image_url", "")

    try:
        resume_id = process_resume_pipeline(image_path, resume_image_url=image_url)
        return jsonify({"message": "Resume processed successfully", "resume_id": resume_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
