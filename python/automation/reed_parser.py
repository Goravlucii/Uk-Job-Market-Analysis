"""
Reed Job Posting Parser — Process Automation
Author: Gaurav Indora
Purpose: Extract structured data from Reed job posting text.
         Parses: salary ranges, skills, experience requirements, remote/hybrid flags.
Usage:   from automation.reed_parser import parse_posting
Skills:  Process Automation, Python, Data Cleaning, Regex
"""
import re, csv, os
from collections import Counter

SKILL_PATTERNS = [
    "SQL","Python","Power BI","Tableau","Excel","R Programming","DAX","Power Query",
    "JIRA","Confluence","Azure","AWS","Machine Learning","Statistical Analysis",
    "Forecasting","Financial Modelling","Business Intelligence","Agile","Scrum",
    "Requirements Gathering","Process Mapping","Stakeholder Management","KPI",
    "ChatGPT","Copilot","Prompt Engineering","VLOOKUP","XLOOKUP","Pivot Table"
]

EXP_PATTERNS = [
    (r"(\d+)\+?\s*year[s]?\s*(?:of\s+)?experience", "years_experience"),
    (r"minimum\s+(\d+)\s+year",                      "years_experience"),
    (r"at\s+least\s+(\d+)\s+year",                   "years_experience"),
    (r"(\d+)\s*-\s*(\d+)\s*year[s]?\s*experience",   "years_range"),
    (r"no\s+experience\s+required",                   "none"),
    (r"fresh\s+graduate[s]?",                         "none"),
    (r"entry[- ]level",                               "entry_level"),
]

SALARY_PATTERN = re.compile(r"£\s*([\d,]+)\s*(?:k|000)?\s*(?:to|[-–])\s*£?\s*([\d,]+)\s*(?:k|000)?", re.IGNORECASE)

def parse_salary(text):
    m = SALARY_PATTERN.search(text)
    if not m: return None, None
    lo = float(m.group(1).replace(",",""))
    hi = float(m.group(2).replace(",",""))
    if lo < 100: lo *= 1000
    if hi < 100: hi *= 1000
    return int(lo), int(hi)

def parse_skills(text):
    found = []
    for skill in SKILL_PATTERNS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text, re.IGNORECASE):
            found.append(skill)
    return found

def parse_experience(text):
    for pattern, label in EXP_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            if label == "none": return 0
            if label == "entry_level": return 0
            if label == "years_experience": return int(m.group(1))
            if label == "years_range": return int(m.group(1))
    return None

def parse_posting(text):
    """Parse a single job posting text and return structured dict."""
    sal_min, sal_max = parse_salary(text)
    skills = parse_skills(text)
    exp = parse_experience(text)
    remote = bool(re.search(r"\b(remote|hybrid|flexible working|work from home|WFH)\b", text, re.IGNORECASE))
    sponsorship = bool(re.search(r"\bvisa\s+sponsor|right\s+to\s+work\b", text, re.IGNORECASE))
    return {
        "salary_min": sal_min, "salary_max": sal_max,
        "skills": skills, "skill_count": len(skills),
        "years_experience_required": exp,
        "requires_experience": exp is not None and exp > 0,
        "remote_hybrid": remote,
        "visa_mentioned": sponsorship,
    }

def batch_parse(input_csv, text_column, output_csv):
    """Parse all postings from a CSV file."""
    rows = []
    with open(input_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            parsed = parse_posting(row.get(text_column,""))
            row.update(parsed)
            rows.append(row)
    with open(output_csv,"w",newline="") as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader(); writer.writerows(rows)
    print(f"Parsed {len(rows)} postings → {output_csv}")

def skill_frequency_report(input_csv, skills_col="skills"):
    """Generate skill frequency report from parsed postings."""
    all_skills = []
    with open(input_csv) as f:
        for row in csv.DictReader(f):
            skills_str = row.get(skills_col,"")
            if skills_str:
                all_skills.extend([s.strip() for s in skills_str.split(";")])
    counts = Counter(all_skills)
    print("\nSkill Frequency Report:")
    print(f"{'Rank':<5} {'Skill':<30} {'Count':<8} {'%'}")
    total_postings = sum(1 for _ in open(input_csv)) - 1
    for rank,(skill,count) in enumerate(counts.most_common(15),1):
        print(f"{rank:<5} {skill:<30} {count:<8} {count/total_postings*100:.1f}%")

if __name__ == "__main__":
    print("Reed Parser ready. Import parse_posting() for single postings.")
    print("Use batch_parse() for CSV files.")
    print("Use skill_frequency_report() to analyse extracted skills.")
