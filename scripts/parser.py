import re

def is_english(text):
    """Returns True if all characters in text are ASCII (English)."""
    return all(ord(char) < 128 for char in text)

def parse_message(text, date):
    # Remove non-English lines
    lines = text.splitlines()
    clean_lines = [line for line in lines if is_english(line.strip()) and line.strip() != '']
    text = "\n".join(clean_lines)

    jjob = {
    "date": date,
    "job_title": None,
    "organization": None,
    "experience": None,
    "max_experience": None,  # <- renamed from location and moved here
    "quantity_required": None,
    "salary": None,
    "gender": None,
    "deadline": None,
    "how_to_apply": None,
    "tags": [],
    "category": None,
    "raw_text": text
}

    # Extract title (first line)
    if clean_lines:
        job["job_title"] = clean_lines[0].strip()

    # Extract tags
    tags = re.findall(r"#\w+", text)
    job["tags"] = ", ".join(tags)
    
    # Organization & Location (next few tags after job title)
    if len(tags) >= 2:
        job["organization"] = tags[0].replace("#", "").replace("_", " ").title()
        job["location"] = tags[-1].replace("#", "").replace("_", " ").title()

    # Experience
    exp_match = re.search(r"#(\d+)_years", text)
    if exp_match:
        job["experience"] = exp_match.group(1)

    # Quantity
    qty_match = re.search(r"Quanitity Required: (\d+)", text)
    if qty_match:
        job["quantity_required"] = qty_match.group(1)

    # Salary
    salary_match = re.search(r"Salary:\s*([\d,\.]+)", text)
    if salary_match:
        job["salary"] = salary_match.group(1)

    # Gender
    gender_match = re.search(r"Required Gender: ([^\n]+)", text)
    if gender_match:
        job["gender"] = gender_match.group(1).strip()

    # Deadline
    deadline_match = re.search(r"Deadline:\s*(.*)", text)
    if deadline_match:
        job["deadline"] = deadline_match.group(1).strip()

    # How to apply
    apply_match = re.search(r"How To Apply:\s*(.*)", text)
    if apply_match:
        job["how_to_apply"] = apply_match.group(1).strip()


    return job
