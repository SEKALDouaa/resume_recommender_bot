from ..models.simple_resume import Resume
from ..extensions import db
import mimetypes

def save_resume_image(resume_id: str, image_path: str):
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "application/octet-stream"

    resume = Resume(id=resume_id, image_data=image_bytes, mime_type=mime_type)
    db.session.merge(resume)  # insert or update
    db.session.commit()

def get_resume_image(resume_id: str):
    return Resume.query.get(resume_id)

def get_all_resume_images():
    resumes = Resume.query.with_entities(Resume.image_data).all()
    return [image_data for (image_data,) in resumes]
