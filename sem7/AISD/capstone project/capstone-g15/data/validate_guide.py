import json
import sys

def validate_guide(guide):
    errors = 0
    section_ids = set()

    if len(guide) < 12 or len(guide) > 20:
        errors += 1
        print("Error: Guide must have 12-20 sections.")

    for section in guide:
        if not all(key in section for key in ["id", "title", "text", "before", "after"]):
            errors += 1
            print("Error: Each section must have 'id', 'title', 'text', 'before', and 'after' fields.")
            continue

        if not section["id"].startswith("G") or not section["id"][1:].isdigit():
            errors += 1
            print(f"Error: Invalid ID '{section['id']}' in section.")
            continue

        if section["id"] in section_ids:
            errors += 1
            print(f"Error: Duplicate ID '{section['id']}' found.")
            continue

        if not section["text"] or len(section["text"]) > 600:
            errors += 1
            print(f"Error: Text field in section '{section['id']}' is empty or exceeds 600 characters.")
            continue

        section_ids.add(section["id"])

    return errors

try:
    with open('data/guide.json', 'r') as f:
        guide = json.load(f)
except FileNotFoundError:
    print("Error: data/guide.json not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: data/guide.json is not valid JSON.")
    sys.exit(1)

errors = validate_guide(guide)

print(f"{len(guide)} sections, {errors} errors")

if errors > 0:
    sys.exit(1)
