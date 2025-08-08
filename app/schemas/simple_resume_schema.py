from ..extensions import ma
from ..models.simple_resume import Resume

class ResumeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Resume
        load_instance = True  # Allows deserialization into model objects

    id = ma.auto_field()
    mime_type = ma.auto_field()
    # Don't serialize raw image_data by default to avoid huge JSON payloads
