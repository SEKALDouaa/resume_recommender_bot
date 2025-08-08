import uuid
from typing import List, Dict, Any
from ..utils.utils import calculate_experience_years

def add_chunk(chunks, resume_id, text, section, image_url, extra_metadata=None):
    if not text.strip():
        return chunks
    chunk_id = str(uuid.uuid4())
    metadata = {"resume_id": resume_id, "resume_section": section, "resume_image": image_url}
    if extra_metadata:
        metadata.update(extra_metadata)
    chunks.append({"id": chunk_id, "text": text.strip(), "metadata": metadata})
    return chunks

def chunk_resume(resume_dict: Dict[str, Any], image_url: str):
    chunks = []
    resume_id = str(uuid.uuid4())

    for section, content in resume_dict.items():
        if not content:
            continue

        if isinstance(content, str):
            chunks = add_chunk(chunks, resume_id, content.replace('\n', ' '), section, image_url)

        elif isinstance(content, list) and all(isinstance(x, str) for x in content):
            for item in content:
                chunks = add_chunk(chunks, resume_id, item, section, image_url)

        elif isinstance(content, list) and all(isinstance(x, dict) for x in content):
            for entry in content:
                if section == "work_experience":
                    metadata = {k: v for k, v in entry.items() if k != "description"}
                    title_line = f"{entry.get('position', '')} at {entry.get('company', '')}"
                    chunks = add_chunk(chunks, resume_id, title_line, section, image_url, metadata)

                    date_line = f"Worked from {entry.get('start month', '')} {entry.get('start year', '')} to {entry.get('end month', '')} {entry.get('end year', '')}"
                    chunks = add_chunk(chunks, resume_id, date_line, section, image_url, metadata)

                    years = calculate_experience_years(
                        entry.get("start month"),
                        entry.get("start year"),
                        entry.get("end month"),
                        entry.get("end year")
                    )
                    if years:
                        metadata["years_of_experience"] = years
                        chunks = add_chunk(chunks, resume_id, f"{years} years of experience in this role", "experience_years", image_url, metadata)

                    for bullet in entry.get("description", []):
                        chunks = add_chunk(chunks, resume_id, bullet, section, image_url, metadata)
                else:
                    combined_text = " ".join(str(v) if not isinstance(v, list) else " ".join(v) for v in entry.values())
                    chunks = add_chunk(chunks, resume_id, combined_text, section, image_url)

    return chunks, resume_id
