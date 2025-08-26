import base64
from flask import Blueprint, Response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.resume_service import get_resume_image, get_all_resume_images
from ..schemas.simple_resume_schema import ResumeSchema

simple_resume_bp = Blueprint("simple_resumes", __name__)
resume_schema = ResumeSchema()

@simple_resume_bp.route("/resume/<resume_id>", methods=["GET"])
@jwt_required()
def get_resume_metadata(resume_id):
    resume = get_resume_image(resume_id)
    if not resume:
        return jsonify({"error": "Resume not found"}), 404
    return resume_schema.dump(resume)

@simple_resume_bp.route("/resume_image/<resume_id>", methods=["GET"])
@jwt_required()
def serve_resume_image(resume_id):
    resume = get_resume_image(resume_id)
    if not resume or not resume.image_data:
        return "Not found", 404
    return Response(resume.image_data, mimetype=resume.mime_type)

@simple_resume_bp.route("/all_resume_images", methods=["GET"])
@jwt_required()
def get_all_resume_images_route():
    images = get_all_resume_images()
    encoded_images = [base64.b64encode(img).decode("utf-8") for img in images]
    return jsonify(encoded_images)
