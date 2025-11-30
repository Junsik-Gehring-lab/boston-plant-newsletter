from pathlib import Path
import yaml
import json
import mkdocs_gen_files

items_dir = Path("docs/items/jobs")
ephemeral_path = Path("docs/.cache/ephemeral.json")

entries = []

# -----------------------------
# ✅ 1. Load PERMANENT job items
# -----------------------------

for path in sorted(items_dir.glob("*.md")):
    text = path.read_text()
    if text.startswith("---"):
        meta = yaml.safe_load(text.split("---", 2)[1])
        title = meta.get("title", path.stem)
        date = meta.get("date", "0000-00-00")
        entries.append({
            "date": date,
            "title": title,
            "path": path.relative_to("docs"),
            "ephemeral": False
        })

# -----------------------------
# ✅ 2. Load EPHEMERAL job items
# -----------------------------

if ephemeral_path.exists():
    with open(ephemeral_path) as f:
        ephemeral_items = json.load(f)

    for item in ephemeral_items:
        if item.get("type") == "job":
            entries.append({
                "date": item.get("source_newsletter", "0000-00-00"),
                "title": item.get("title"),
                "path": f"newsletter/{item.get('source_file')}",
                "ephemeral": True
            })

# -----------------------------
# ✅ 3. Sort ALL jobs together
# -----------------------------

from datetime import date

def normalize_date(d):
    # If already a datetime.date → keep it
    if isinstance(d, date):
        return d
    # If string like "2025-02-07" → convert to date
    try:
        return date.fromisoformat(d)
    except Exception:
        return date(1900, 1, 1)  # final fallback for safety

entries.sort(key=lambda x: normalize_date(x["date"]), reverse=True)

# -----------------------------
# ✅ 4. Write FINAL jobs.md
# -----------------------------

with mkdocs_gen_files.open("jobs.md", "w") as f:
    f.write("# 🧬 Job Opportunities\n\n")
    f.write("This page is generated automatically from permanent items and newsletters.\n\n---\n\n")

    for item in entries:
        if item["ephemeral"]:
            f.write(f"- 📰 **{item['title']}** *(from newsletter)* → [{item['path']}]({item['path']})\n")
        else:
            f.write(f"- [{item['title']}]({item['path']})\n")
