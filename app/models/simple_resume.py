from ..extensions import db

class Resume(db.Model):
    __tablename__ = "resumes"

    id = db.Column(db.String, primary_key=True)
    image_data = db.Column(db.LargeBinary, nullable=False)  # raw bytes
    mime_type = db.Column(db.String, nullable=False)        # e.g. "image/jpeg"
