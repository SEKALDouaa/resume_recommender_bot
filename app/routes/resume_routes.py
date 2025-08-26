from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.resume_pipeline_service import process_resume_pipeline
import traceback
import os

resume_bp = Blueprint("resume", __name__)

@resume_bp.route("/process-resume", methods=["POST"])
@jwt_required()
def process_resume():
    if 'images' not in request.files:
        return jsonify({"error": "No image files provided"}), 400

    images = request.files.getlist("images")
    processed_resumes = []
    current_user = get_jwt_identity()

    try:
        for image in images:
            image_path = f"/tmp/{image.filename}"
            image.save(image_path)

            image_url = request.form.get("image_url", "")  

            resume_id = process_resume_pipeline(
                image_path,
                resume_image_url=image_url
            )
            processed_resumes.append({
                "filename": image.filename,
                "resume_id": resume_id
            })

        return jsonify({
            "message": f"{len(processed_resumes)} resumes processed successfully",
            "user": current_user,
            "resumes": processed_resumes
        })

    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        return jsonify({"error": str(e), "traceback": tb}), 500
