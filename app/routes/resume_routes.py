from services.resume_pipeline_service import process_resume_pipeline

@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    # Save image
    image_file = request.files["resume"]
    image_path = save_uploaded_file(image_file)  # you’ll write this helper
    resume_id = process_resume_pipeline(image_path, resume_image_url=image_path)
    return jsonify({"status": "success", "resume_id": resume_id})
