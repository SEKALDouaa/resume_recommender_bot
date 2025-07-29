import difflib
import re
import json

with open(r"C:\Dev\resume_recommender_bot\data\job_positions\job_titles.json", "r", encoding="utf-8") as f:
    known_titles = json.load(f)

if isinstance(known_titles, dict) and "job-titles" in known_titles:
    known_titles = [title.lower().strip() for title in known_titles["job-titles"]]
else:
    raise ValueError("Expected a dictionary with a 'titles' key containing a list.") 

text = 'David Villatoro\n\nWeb Designer / Developer with 5 years of experience in the design and development of innovative\nstaticand dynamic websites using current W3C standards of coding. Additional experience in the use of\ncontent management systems toallow clients toupdate content on their websites. Very strong,\n‘organizational, presentational, and communication sill to help plan out and pitch different web user\nInterface styles that suited the cient’ needs.\n\nEDUCATION\nBA in Interactive Entertainment, Minor in 3D Animation - Unversity of Southern California, 2008\nTECHNICAL skis\nWeb Programming\nXHTML, CSS, Javascrit, jQuery, XML/RSS Feed, PHP, MySQL, Actionscript 3.0 Light HFML5/CSS3\nSoftware\n\n‘Adobe Dreamweaver C55, Adobe Photoshop CSS, Adobe Flash CSS,\n\n‘Content Management Systems\nWordpress, Joomla, Adobe C5, Jive\n\nOther Relevant Sills\nLeadership, Organization, Communication, Self-motivated, Team oriented, Productivity, Problem.\nsolving sil, Blingual (English and Spanish)\n\nEXPERIENCE\n\nFront End Web Developer, Activision] Blizzard March 2012 ~Present\n\n> Developed websites with Adobe CO allowing the developing team to create reusable\n‘components that can be easily used to build outthe sites.\n> Used Jive to develop custom themes that would be applied to community forums and blogs\n\n‘WebDeveloper, Unbutton it ‘April 2011 ~ October 2011\n\n> Collaborated witha web designer to program the entire site using XHTML, CSS, PHP, MySQl,\n‘and jQuery from PSD files.\n\n> Developed a custom shopping cart system to receive transactions from customers which can\nbe viewed from a custom made content management system made for the dient.\n'

lines = [line.strip() for line in text.split('\n') if line.strip()]

# for line in lines: 
#     print(line)
#     print('')

def is_known_section (line, cutoff= 0.8):
    known_sections = {
        "WORK EXPERIENCE", "CONTACT", "SKILLS","TECHNICAL SKILLS", "EDUCATION", "OTHER", "PROJECTS",
        "EXPERIENCE", "CERTIFICATIONS", "LANGUAGES", "SUMMARY", "OBJECTIVE", "STRENGTHS", "MY LIFE PHILISOPHY"
    }
    match = difflib.get_close_matches(line.upper(), known_sections, n=1, cutoff=cutoff)
    return match[0] if match else None

def is_noise (line):
    noise_keywords = ["powered by", "enhancv", "resume.io", "novoresume", "cv builder", "zety"]
    line_lower = line.lower().strip()

    if re.fullmatch (r"https?://\S+", line.strip()) and not any (domain in line_lower for domain in ["github", "linkedin"]):
        return True
    
    if any(keyword in line_lower for keyword in noise_keywords):
        return True

    return False            

def normalize_bullets(line):
    bullets = ['•', '-', '–', '*', '»', '+', '©', 'e ', '_']
    for bullet in bullets:
        if line.strip().startswith(bullet):
            return "- " + line[1:].strip()
    return line
lines = [normalize_bullets(line) for line in lines]

def is_title(line):
    is_title = False
    uppercase_count = sum(1 for c in line if c.isupper())/len(line)
    uppercase_ratio = uppercase_count/len(line)
    if len(line) < 20 and uppercase_count!=0 and line[0] != '-' and (line[-1:] not in [':','.', '!', '?',';'] or line.isupper() or uppercase_ratio > 0.5):
        is_title = True
    return is_title

def flush (structure, section, subsection, buffer):
    '''puts any content in the buffer into its right place in the structure'''
    if not buffer: 
        return
    
    if section not in structure: 
        structure[section] = []
    
    if isinstance(structure[section], list):
        structure[section].append(buffer)
    
    elif isinstance(structure[section], dict):
        if subsection :
            if subsection not in structure[section]:
                structure[section][subsection] = []
            structure[section][subsection].append(buffer)

        else:
            structure[section]["UNKNOWN"] = buffer

def extract_structure(lines):
    structure = {}
    current_section = "Personal Information"
    current_subsection = None
    buffer = []

    for line in lines:
        if is_noise(line):
            continue
        if is_title(line):
            matched_section = is_known_section(line)

            if matched_section:
                flush(structure, current_section, current_subsection, buffer)
                current_section = matched_section
                current_subsection = None
                buffer = []
                structure[current_section] = {}
        
            else:
                flush(structure, current_section, current_subsection, buffer)
                current_subsection = line
                buffer = []

        else:
            buffer.append(line)
        
    flush(structure, current_section, current_subsection, buffer)
    return structure

def merge_lines(lines):
    merged = []
    buffer = ""
    for line in lines:
        if is_noise(line):
            continue
        line = line.strip()
        if not line:
            continue
        elif not buffer:
            buffer = line
        elif line.startswith("-") or line[0].isupper():
            merged.append(buffer)
            buffer = line
        else:
            buffer += " " + line
    if buffer:
        merged.append(buffer)
    return merged

def recursive_merge(content):
    if isinstance(content, dict):
        for key, val in content.items():
            content[key] = recursive_merge(val)
        return content
    elif isinstance(content, list):
        if content and all(isinstance(item, list) for item in content):
            return [merge_lines(block) for block in content]
        else:
            return merge_lines(content)
    else:
        return content
    
refined_sectionned_lines = extract_structure(lines)    
refined_sectionned_lines = recursive_merge(refined_sectionned_lines)

def extract_dates(line):
    MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
    normalized_line = line.strip()
    pattern_full = re.compile(
            r"\b(" + "|".join(MONTHS) + r")\s(\d{4})\s*(?:-|–|to)\s*(?:" +
            r"(" + "|".join(MONTHS) + r")\s(\d{4})|(?P<end_open>Present|Ongoing))\b",
            re.IGNORECASE
        )
    pattern_year_only = re.compile(r"\b(\d{4})\s*(?:-|–|to)\s*(\d{4}|Present|Ongoing)\b", re.IGNORECASE)
    match1 = pattern_full.search(normalized_line)
    if match1:
        return {
            "start month": match1.group(1),
            "start year": match1.group(2),
            "end month": match1.group(3) or match1.group("end_open"),
            "end year": match1.group(4) or None
        }
    match2 = pattern_year_only.search(normalized_line)
    if match2:
        return{
        "start month": None,
        "start year": match2.group(1),
        "end month": None,
        "end year": match2.group(2) or None
        }
    
def find_job_title(line, cutoff=0.8):
    line = line.lower().strip()
    print("🔍 Trying to match line:", repr(line))
    match = difflib.get_close_matches(line, known_titles, n=1, cutoff=cutoff)
    print("🎯 Match:", match)    
    return match[0] if match else None

def process_block(block):
    entry = { 
        "position" : None, "company" : None, "dates" : None, "description" : []
    }

    if not block: 
        return None
    date_pattern = re.compile(
            r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)?\s*\d{4}\s*(?:-|–|to)\s*(?:\b(?:January|February|March|April|May|June|July|August|September|October|November|December)?\s*\d{4}|Present|Ongoing)\b",
            re.IGNORECASE
        )
     
    for i, line in enumerate(block):
        if extract_dates(line):
            entry["dates"] = extract_dates(line)
        cleaned_line = date_pattern.sub("", line).strip()
        block[i] = cleaned_line if cleaned_line else ""
        break
    print (f"Processing block: {block}")

    for i,line in enumerate(block):
        title = find_job_title(line)
        if title:
            entry["position"] = title
            del block[i]
            break
    
    block = [line for line in block if line.strip()]
    num_capitals = sum(1 for c in block[0] if c.isupper())
    if num_capitals > 1 and not block[0].strip().startswith("-"):
        entry["company"] = block[0]
        del block[0]
    
    description_lines  = [line for line in block]
    entry["description"] = [line.lstrip("-").strip() for line in description_lines]

    return entry if any(entry.values()) else None

    
def parse_experience_block(lines):
    parsed = []
    block = []

    for line in lines + [""]:
        is_new_block = find_job_title(line) or extract_dates(line)
        if  is_new_block and block:
            entry = process_block(block)
            if entry:
                parsed.append(entry)
            block = []
        block.append(line)
        
    if block:
        entry = process_block(block)
        if entry:
            parsed.append(entry)

    return parsed 

print(">> BEFORE PARSING EXPERIENCE BLOCK")
print("TYPE:", type(refined_sectionned_lines["EXPERIENCE"]["UNKNOWN"]))
print("CONTENT:")
for item in refined_sectionned_lines["EXPERIENCE"]["UNKNOWN"]:
    print(item)
    
refined_sectionned_lines["EXPERIENCE"]["UNKNOWN"] = parse_experience_block(refined_sectionned_lines["EXPERIENCE"]["UNKNOWN"])

i = 0
for section, content in refined_sectionned_lines.items():
    i += 1
    print(f"\n{section.upper()} {i}")

    if isinstance(content, dict):
        for sub, lines in content.items():
            print(f"  {sub}:")
            if isinstance(lines, list):
                for item in lines:
                    if isinstance(item, str):
                        print(f"    {item}")
                    elif isinstance(item, dict):
                        for key, val in item.items():
                            if isinstance(val, dict):
                                print(f"    {key}:")
                                for k, v in val.items():
                                    print(f"      {k}: {v}")
                            else:
                                print(f"    {key}: {val}")
                    else:
                        print(f"    {item}")
            else:
                print(f"    {lines}")

    elif isinstance(content, list):
        for line in content:
            if isinstance(line, str):
                print(f"  {line}")
            elif isinstance(line, dict):
                for key, val in line.items():
                    print(f"  {key}: {val}")
            else:
                print(f"  {line}")

    else:
        print(f"  {content}")
