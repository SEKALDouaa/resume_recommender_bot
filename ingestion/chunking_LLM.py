import google.generativeai as genai
from decouple import config
import re

raw_text = "First Last\n\nJunior Business Analyst\n\nBusiness analyst with 10 years of experience in business analysis, file processing,\nbusiness process documentation, system testing, requirement gathering, and data\nanalysis. Key achievements: collaborated with the sales team to create a new system that\nimproved customer satisfaction by 60% YoY. Provided analysis for a $500K business\nenterprise for the successful launch of 15 new projects in Q1, 2014.\n\nWORK EXPERIENCE\n\nJunior Business Analyst November 2015 — Present\nResume Worded, New York, NY\n\ne Assisted with developing 14 new products, which resulted in a\nrevenue of $950K within 5 weeks of launch.\n\ne Developed an automated reporting tool tracking sales pipeline data\nacross 11 channels, including web, email, and phone—this project\nreduced time spent on manual entry from 72 hours per month to 30\nminutes per week.\n\ne Concocted an automated process that tracked and reported on key\nbusiness metrics, increasing productivity by 80% the first time after\n15 years.\n\ne Collaborated with the sales team to create a new system that\nimproved customer satisfaction by 60% YoY.\n\nCost Analyst February 2013 — October 2015\nGrowthsi, San Francisco, CA\n\ne Increased the company’s ROI while reducing development time by\n85% by studying change requests, determining issues, prioritizing, and\ndevising solutions.\n\ne Created monthly forecasts, PL statements, balance sheet reports, and\ncash flow statements for 100 HNls using Crystal Reports.\n\ne Helped develop cost estimates that generated a budget savings of\n$182K by reducing the overhead as part of the company's corporate\nrestructuring.\n\ne Provided analysis for a SSOOK business enterprise for the successful\nlaunch of 15 new projects in Q1, 2014.\n\nStudent Research Assistant June 2010 — January 2013\nResume Worded's Exciting Company, New York, NY\n\ne Collaborated with 400 research participants in 19 counties by\ncomplying with all ethical guidelines.\n\ne Tracked down pertinent information from 1.5K sources by utilizing\nlibrary and internet research.\n\ne Coached 75 colleagues on using an electronic database search\nsystem to locate evidence-based educational articles.\n\ne Streamlined the company's research process by developing an\nelectronic database management program that saved 300\nresearchers over 2 weeks of manual labor per month.\n\nCONTACT\n\n- Seattle, WA (Open to Remote)\n- +1-234-456-789\n\n- email@resumeworded.com\n\n» linkedin.com/in/username\n\n- github.com/resumeworded\n\nSKILLS\n\nTechnical Skills:\n\n- Consulting (Advanced)\n\n- Integration (Experienced)\n- Data Analysis\n\n- Strategic Planning\n\n» Testing\n\nIndustry Knowledge:\n\n- Data Visualization\n\n- Requirements Engineering\n- Business Requirements\n\nTools and Software:\n- SharePoint\n\n+ PRINCE2\n\n» MySQL\n\n+ Microsoft Power BI\n© ITIL\n\n- Don't forget to use Resume\nWorded to scan your resume\nbefore you send it off (it’s free and\nproven to get you more jobs)\n\nEDUCATION\n\nResume Worded University\n\nBachelor of Science\nBusiness Administration\nBoston, MA — May 2010\n\nAwards: Resume Worded Teaching\nFellow (only 5 awarded to class), Dean’s\nList 2012 (Top 10%)\n\nOTHER\n\n- Certified Business Analyst.\n\n- Certified ScrumMaster (CSM).\n- Certified Associate in Project\nManagement (CAPM).\n"
genai.configure(api_key=config("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def order_resume_into_dictionary(raw_text):
    prompt = f"""
    You are a resume parser. Your job is to extract structured data from raw resume text and return it as a valid **Python dictionary** (not JSON).

    Use the following schema:

    - `name`: Full name at the top.
    - `title`: Job title directly under the name.
    - `summary`: Paragraph before the WORK EXPERIENCE section.
    - `work_experience`: a list of entries. Each entry must include all of these keys (even if the value is missing, use None):
        {{
        "position": str or None,
        "company": str or None,
        "start month": str or None,
        "start year": int or None,
        "end month": str or None,
        "end year": int or "Present" or None,
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
    - Always include all keys for `work_experience` entries, even if their values are unknown (`None`).
    - For dates, extract the month and year if available.
    - If an end date is missing or the job is ongoing, use `"end month": None` and `"end year": "Present"`.
    - Remove all newline characters (`\\n`) **inside** text values by replacing them with a single space, so that sentences and bullet points are continuous and clean.
    - Preserve line breaks only between list items or sections, but do not include `\\n` inside individual strings.
    Here is the resume text:
    {raw_text}
    """
    response = model.generate_content(prompt)
    text = response.text.strip()
    text = re.sub(r"^```(?:python)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()
    

chunked_text = order_resume_into_dictionary(raw_text)
print(chunked_text)