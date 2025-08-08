from flask import Blueprint, Response, jsonify
from ..services.resume_service import get_resume_image
from ..schemas.simple_resume_schema import ResumeSchema

simple_resume_bp = Blueprint("simple_resumes", __name__)
resume_schema = ResumeSchema()

@simple_resume_bp.route("/resume/<resume_id>", methods=["GET"])
def get_resume_metadata(resume_id):
    resume = get_resume_image(resume_id)  # returns Resume object or None
    if not resume:
        return jsonify({"error": "Resume not found"}), 404
    # serialize metadata only (exclude image_data)
    return resume_schema.dump(resume)

@simple_resume_bp.route("/resume_image/<resume_id>", methods=["GET"])
def serve_resume_image(resume_id):
    resume = get_resume_image(resume_id)  # returns Resume object or None
    if not resume or not resume.image_data:
        return "Not found", 404
    return Response(resume.image_data, mimetype=resume.mime_type)
