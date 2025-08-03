import google.generativeai as genai
from decouple import config
import re
import uuid
from typing import Dict, List, Any, Optional
import ast
from datetime import datetime


raw_text = "First Last\n\nJunior Business Analyst\n\nBusiness analyst with 10 years of experience in business analysis, file processing,\nbusiness process documentation, system testing, requirement gathering, and data\nanalysis. Key achievements: collaborated with the sales team to create a new system that\nimproved customer satisfaction by 60% YoY. Provided analysis for a $500K business\nenterprise for the successful launch of 15 new projects in Q1, 2014.\n\nWORK EXPERIENCE\n\nJunior Business Analyst November 2015 — Present\nResume Worded, New York, NY\n\ne Assisted with developing 14 new products, which resulted in a\nrevenue of $950K within 5 weeks of launch.\n\ne Developed an automated reporting tool tracking sales pipeline data\nacross 11 channels, including web, email, and phone—this project\nreduced time spent on manual entry from 72 hours per month to 30\nminutes per week.\n\ne Concocted an automated process that tracked and reported on key\nbusiness metrics, increasing productivity by 80% the first time after\n15 years.\n\ne Collaborated with the sales team to create a new system that\nimproved customer satisfaction by 60% YoY.\n\nCost Analyst February 2013 — October 2015\nGrowthsi, San Francisco, CA\n\ne Increased the company’s ROI while reducing development time by\n85% by studying change requests, determining issues, prioritizing, and\ndevising solutions.\n\ne Created monthly forecasts, PL statements, balance sheet reports, and\ncash flow statements for 100 HNls using Crystal Reports.\n\ne Helped develop cost estimates that generated a budget savings of\n$182K by reducing the overhead as part of the company's corporate\nrestructuring.\n\ne Provided analysis for a SSOOK business enterprise for the successful\nlaunch of 15 new projects in Q1, 2014.\n\nStudent Research Assistant June 2010 — January 2013\nResume Worded's Exciting Company, New York, NY\n\ne Collaborated with 400 research participants in 19 counties by\ncomplying with all ethical guidelines.\n\ne Tracked down pertinent information from 1.5K sources by utilizing\nlibrary and internet research.\n\ne Coached 75 colleagues on using an electronic database search\nsystem to locate evidence-based educational articles.\n\ne Streamlined the company's research process by developing an\nelectronic database management program that saved 300\nresearchers over 2 weeks of manual labor per month.\n\nCONTACT\n\n- Seattle, WA (Open to Remote)\n- +1-234-456-789\n\n- email@resumeworded.com\n\n» linkedin.com/in/username\n\n- github.com/resumeworded\n\nSKILLS\n\nTechnical Skills:\n\n- Consulting (Advanced)\n\n- Integration (Experienced)\n- Data Analysis\n\n- Strategic Planning\n\n» Testing\n\nIndustry Knowledge:\n\n- Data Visualization\n\n- Requirements Engineering\n- Business Requirements\n\nTools and Software:\n- SharePoint\n\n+ PRINCE2\n\n» MySQL\n\n+ Microsoft Power BI\n© ITIL\n\n- Don't forget to use Resume\nWorded to scan your resume\nbefore you send it off (it’s free and\nproven to get you more jobs)\n\nEDUCATION\n\nResume Worded University\n\nBachelor of Science\nBusiness Administration\nBoston, MA — May 2010\n\nAwards: Resume Worded Teaching\nFellow (only 5 awarded to class), Dean’s\nList 2012 (Top 10%)\n\nOTHER\n\n- Certified Business Analyst.\n\n- Certified ScrumMaster (CSM).\n- Certified Associate in Project\nManagement (CAPM).\n"
genai.configure(api_key=config("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
def calculate_experience_years(start_month, start_year, end_month,end_year):
    try:
        start = datetime.strptime(f"{start_month or 'January'} {start_year}", "%B %Y")
        if end_year == "Present":
            end = datetime.now()
        else:
            end = datetime.strptime(f"{start_month or 'January'} {end_year}", "%B %Y")
        delta = end - start
        return round(delta.days/365.25,1)
    except Exception:
        return None
    
def order_resume_into_dictionary(raw_text):
    prompt = f"""
    You are a resume parser. Your job is to extract structured data from raw resume text and return it as a valid **Python dictionary** (not JSON).

    Use the following schema:

    - `name`: Full name at the top.
    - `title`: Job title directly under the name.
    - `summary`: Paragraph before the WORK EXPERIENCE section.
    - `work_experience`: a list of entries. Each entry must include all of these keys (even if the value is missing, use "". Never use None):
        {{
        "position": str (use empty string `""` if missing),
        "company": str (use empty string `""` if missing),
        "start month": str (use empty string `""` if missing),
        "start year": int or `""` (if unknown),
        "end month": str (use empty string `""` if missing),
        "end year": int, "Present", or `""` (if unknown),
        "description": list of bullet points (can be empty)
        }}
    - `education`: A single multi-line string containing all education-related information.
    - `skills`: A flat list of all skills found (ignore categories like "Technical Skills" — just extract the items).
    - `contact`: A dictionary with only the keys found in the text. Valid keys:
        - `location`
        - `phone`
        - `email`
        - `linkedin`
        - `github`

        Omit any contact field that is missing. Do **not** use null or None in contact fields.

    - `other`: A list of any information that does not fit in the above sections (certifications, references, tips, etc.).

    Instructions:
    - Do not fabricate any content.
    - If any value is missing or unknown, use `""` or `[]`, not `None` or `null`.
    - For dates, extract the month and year if available.
    - If an end date is missing or the job is ongoing, use `"end month": ""` and `"end year": "Present"`.
    - Remove all newline characters (`\\n`) **inside** text values by replacing them with a single space, so that sentences and bullet points are continuous and clean.
    - Preserve line breaks only between list items or sections, but do not include `\\n` inside individual strings.
    Here is the resume text:
    {raw_text}
    """
    response = model.generate_content(prompt)
    text = response.text.strip()
    text = re.sub(r"^```(?:python)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return ast.literal_eval(text.strip())
    

chunked_dict = order_resume_into_dictionary(raw_text)

def add_chunk(chunks: List, resume_id: str, text:str, section: str, resume_image_url: str, extra_metadata: Dict = None):
    if not text.strip():
        return
    
    chunk_id = str(uuid.uuid4())
    metadata = {
        "resume_id" : resume_id,
        "resume_section": section,
        "resume_image": resume_image_url
    }

    if extra_metadata:
        metadata.update(extra_metadata)
    
    chunks.append({
        "id": chunk_id,
        "text": text.strip(),
        "metadata": metadata
    })
    return chunks
  
def chunk_resume(resume_dict: Dict[str, Any],resume_image_url: str) -> List[Dict[str,Any]]:
    chunks = []
    resume_id = str(uuid.uuid4())

    for section, content in resume_dict.items():
        if not content:
            continue

        if isinstance(content, str):
            clean_text = content.replace('\n',' ')
            chunks = add_chunk(chunks, resume_id, clean_text, section, resume_image_url)
        
        elif isinstance(content, list) and all(isinstance(x,str) for x in content):
            for item in content: 
                chunks = add_chunk(chunks, resume_id, item, section, resume_image_url)
       
        elif isinstance(content, list) and all(isinstance(x,dict) for x in content):
            for entry in content:
                if section == 'work_experience':
                    metadata = {k: v for k, v in entry.items() if k != "description"}

                    # 1. Chunk position and company
                    title_line = f"{entry.get('position', 'Unknown Position')} at {entry.get('company', 'Unknown Company')}"
                    chunks = add_chunk(chunks, resume_id, title_line, section, resume_image_url, metadata)

                    # 2. Chunk date range
                    start = f"{entry.get('start month', '')} {entry.get('start year', '')}".strip()
                    end = f"{entry.get('end month', '')} {entry.get('end year', '')}".strip()
                    date_line = f"Worked from {start} to {end}".strip()
                    chunks = add_chunk(chunks, resume_id, date_line, section, resume_image_url, metadata)

                    # 3. Chunk years_of_experience as separate text chunk
                    years = calculate_experience_years(
                        entry.get("start month"),
                        entry.get("start year"),
                        entry.get("end month"),
                        entry.get("end year"),
                    )
                    if years is not None:
                        metadata["years_of_experience"] = years
                        years_text = f"{years} years of experience in this role"
                        chunks = add_chunk(
                            chunks,
                            resume_id,
                            years_text,
                            "experience_years",
                            resume_image_url,
                            metadata
                        )


                    # 4. Chunk each description bullet separately
                    if entry.get("description"):
                        for bullet in entry["description"]:
                            chunks = add_chunk(chunks, resume_id, bullet, section, resume_image_url, metadata)

                else:
                    # For other sections with dict entries fallback to original approach
                    entry_text_parts = []
                    metadata = {}
                    for k, v in entry.items():
                        if isinstance(v, list):
                            text = ' '.join(v)
                            entry_text_parts.append(text)
                        elif v:
                            entry_text_parts.append(str(v))
                            metadata[k] = v
                    combined_text = " ".join(entry_text_parts)
                    chunks = add_chunk(chunks, resume_id, combined_text, section, resume_image_url, metadata)
        
        else: 
            chunks = add_chunk(chunks, resume_id, str(content), section, resume_image_url)
    return chunks, resume_id
resume_to_embed, resume_id = chunk_resume(chunked_dict, "/data/tbhidkthepath")

#print(f"The resume id is: {resume_id} \n The chunked resume is: {resume_to_embed}")

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')


import chromadb

chroma_client = chromadb.PersistentClient(path="chroma_db")

collection = chroma_client.get_or_create_collection(name='resumes')

texts = [chunk["text"] for chunk in resume_to_embed]
ids = [chunk["id"] for chunk in resume_to_embed]
metadatas = [chunk["metadata"] for chunk in resume_to_embed]

embeddings = model.encode(texts).tolist()

collection.add(documents=texts, metadatas= metadatas,ids= ids, embeddings= embeddings)

query = "Business analyst with reporting experience"
query_embedding = model.encode([query]).tolist()

results = collection.query(query_embeddings = query_embedding, n_results= 5)
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print("Match:", doc)
    print("Metadata:", meta)
    print("-----")