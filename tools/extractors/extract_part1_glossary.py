"""
Extractor for Part 1: Rules Glossary (Appendix C & Chapter 1).
Extracts all terms and descriptions from DnD 5,5e 2024 PHB.md into rules/glossary.json.
"""

import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PHB_PATH = ROOT / "DnD 5,5e 2024 PHB.md"
OUTPUT_PATH = ROOT / "rules" / "glossary.json"


def extract_glossary():
    with open(PHB_PATH, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()[39310:41474]

    glossary = {}
    current_term = None
    current_body = []

    for line in lines:
        m = re.match(r"^#{2,4}\s+([A-Za-z0-9\s\-\'\"/(),]+)", line)
        if m and not line.startswith("### APPENDIX") and not line.startswith("## Index") and not line.startswith("## Appendix"):
            title = m.group(1).strip()
            clean_title = re.sub(r"\[.*?\]", "", title).strip()
            if clean_title:
                if current_term and current_body:
                    body_txt = "\n".join(current_body).strip()
                    body_txt = re.sub(r"APPENDI[X\s]+[A-Z0-9\s!|j]+\n?", "", body_txt)
                    body_txt = re.sub(r"<!-- Page \d+ -->\n?", "", body_txt)
                    key = current_term.lower().replace(" ", "_").replace("-", "_")
                    if key not in glossary or len(body_txt) > len(glossary[key].get("description", "")):
                        glossary[key] = {
                            "name": current_term,
                            "description": body_txt,
                            "source": "PHB 2024 Appendix C (Rules Glossary)"
                        }
                current_term = clean_title
                current_body = []
        else:
            current_body.append(line)

    if current_term and current_body:
        body_txt = "\n".join(current_body).strip()
        body_txt = re.sub(r"APPENDI[X\s]+[A-Z0-9\s!|j]+\n?", "", body_txt)
        body_txt = re.sub(r"<!-- Page \d+ -->\n?", "", body_txt)
        key = current_term.lower().replace(" ", "_").replace("-", "_")
        glossary[key] = {
            "name": current_term,
            "description": body_txt,
            "source": "PHB 2024 Appendix C (Rules Glossary)"
        }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(glossary, f, indent=2)

    print(f"Extracted {len(glossary)} glossary terms to {OUTPUT_PATH}")
    return glossary


if __name__ == "__main__":
    extract_glossary()
