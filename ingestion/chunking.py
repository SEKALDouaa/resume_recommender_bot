
text = 'TAYLOR FOSTER\nBig Data Scientist\n\n1-324-677-8914 taylor51@gmail.com colossal-mattress.org\nNorth Milanworth, Greece\n\nSUMMARY\n\nExperienced Big Data Scientist with 10+ years of experience in ingesting,\nstoring, processing, and analyzing large datasets. Skilled in developing\nscalable data solutions, optimizing data processing efficiency, and\nleveraging industry-leading tools like Tableau and R for data visualization.\nProficient in Java, Scala, and Spark, with expertise in AWS cloud platform.\nStrong problem-solving and collaboration abilities, demonstrated through\nsuccessful project outcomes and mentoring junior team members. Master\nof Science in Data Science from the University of California, Berkeley. Most\nproud of developing an automated data cleansing tool and deploying a real-\ntime fraud detection system resulting in significant cost savings. Passionate\nabout unlocking the hidden value of data to drive innovation.\n\nEXPERIENCE\n\nSenior Data Engineer 2022 - Ongoing\n\nTech Innovators San Francisco, CA\n\nLed the development and implementation of data pipelines, resulting in a 30%\n\nincrease in data processing efficiency.\n\n* Collaborated with cross-functional teams to understand business\nrequirements and design scalable data solutions.\n\n* Optimized data storage and processing techniques, reducing resource\nutilization by 20%.\n\n* Mentored junior engineers, providing technical guidance and training to\nenhance their skills and productivity.\n\nData Scientist 2017 - 2022\n\nData Analytics Inc. New York, NY\n\nPerformed extensive data analysis and modeling, resulting in improved insights\n\nand data-driven decision-making.\n\n* Developed and implemented machine learning algorithms to predict customer\nbehavior, increasing revenue by 15%.\n\n* Collaborated with stakeholders to identify and define key performance\nindicators, aligning analytics goals with business objectives.\n\n* Utilized Tableau to create interactive visualizations, facilitating the\ncommunication of complex data insights.\n\nPowered by (CX? Enhancu\n\nwww.enhancv.com\n\nY LIFE PHILOSOPHY\n\nData is the new gold. As a Big\nData Scientist, | strive to\nunlock its hidden value and\ndrive data-powered\ninnovation.\n\nSTRENGTHS\n\n® Problem Solving\n\nExperienced in identifying\ncomplex issues and\ndeveloping innovative\nsolutions resulting in\nimproved data analysis and\nefficiency.\n\nCollaboration\n\nProven ability to work\ncollaboratively with cross-\nfunctional teams, providing\nvaluable insights and driving\nsuccessful project outcomes.\n\nAdaptability\n\nDemonstrated flexibility in\nadapting to new technologies\nand evolving business needs,\nensuring the delivery of high-\nquality data solutions.\n\nSKILLS\n\nBig Data Technologies - Java-\nScala - Spark - Data Warehousing -\nData Modeling: Tableau: R -\nAWS - Kafka - Core Java: Scripting\n\n'

lines = [line.strip() for line in text.split('\n') if line.strip()]

# for line in lines: 
#     print(line)
#     print('')

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

def extract_sections(lines):
    sections = {}
    sections["Name"] = lines[0] 
    current_title = "Personal Information"
    sections[current_title] = []
    for line in lines[1:]:
        if is_title(line):
            current_title = line 
            sections[current_title] = []
        else:
            sections[current_title].append(line)

    return sections

sectionned_lines = extract_sections(lines)

def merge_lines(lines):
    merged = []
    buffer = ""
    for line in lines:
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

for section, content in sectionned_lines.items():
    if isinstance(content, list):
        sectionned_lines[section] = merge_lines(content)

# i = 0
# for section, content in sectionned_lines.items():
#     print(f"{section}: {i}")
#     if isinstance(content, str):
#         print(f"  {content}")
#     else:
#         for line in content:
#             print(f"  {line}")
#         print("")
#     i += 1

def extract_subsections(sectionned_lines):
    known_subsections = { "WORK EXPERIENCE", "CONTACT", "SKILLS", "EDUCATION", "OTHER", "PROJECTS",
        "EXPERIENCE", "CERTIFICATIONS", "LANGUAGES", "SUMMARY", "OBJECTIVE" }
    refined_subsections = {}
    for section, content in sectionned_lines.items():

        if not isinstance(content, list):
            refined_subsections[section] = content
            continue

        subsections = {}
        current_sub = None
        buffer = []

        i = 0 
        while i < len(content):
            line = content[i]

            if len(line) < 20 and (i+1) < len(content) and content[i+1].strip().startswith("-"):
                if current_sub and buffer:
                    subsections[current_sub] = buffer
                    buffer = []

                current_sub = line.rstrip(":")
                i += 1 
                bullets = []
                while i < len(content) and content[i].strip().startswith("-"):
                    bullets.append(content[i].strip())
                    i += 1
                
                subsections[current_sub] = bullets
                continue

            elif len(line) < 25 and not line.startswith("-") and line.upper() not in known_subsections:
                if current_sub and buffer:
                    subsections[current_sub] = buffer
                    buffer = []

                current_sub = line
                i += 1
                continue

            elif is_title(line) and line.upper() not in known_subsections:
                if buffer and current_sub:
                    subsections[current_sub] = buffer
                    buffer = []
                
                current_sub = line
                i += 1 
                continue

            elif is_title(line) and line.upper() in known_subsections:
                break

                # while i < len(content) and content[i] not in known_subsections:
                #     if is_title(content[i]):
                #         if buffer and current_sub:
                #             subsections[current_sub] = buffer
                #             buffer = []
                #             current_sub = content[i]
                #             continue
                #     else:
                #         buffer.append(content[i])
                #     i += 1 
                #     subsections[current_sub] = buffer
                #     buffer = []
                #     continue
            else:
                if is_title(line) and line.upper() not in known_subsections:
                    if current_sub and buffer:
                        subsections[current_sub] = buffer
                        buffer = []
                    current_sub = line
                    i += 1
                else:
                    buffer.append(line)
                    i += 1
                    
        if current_sub and buffer:
            subsections[current_sub] = buffer
            
        refined_subsections[section] = subsections if subsections else content
    return refined_subsections

refined_sectionned_lines = extract_subsections(sectionned_lines)

i=0 
for section, content in refined_sectionned_lines.items():
    i += 1
    print(f"\n{section.upper()} {i}")
    if isinstance(content, dict):
        for sub, lines in content.items():
            print(f"  {sub}: {i}")
            for line in lines:
                print(f"    {line}")
    elif isinstance(content, list):
        for line in content:
            print(f"  {line}")
    else:
        print(f"  {content}")