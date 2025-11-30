from pathlib import Path
import yaml
import json
import mkdocs_gen_files
from datetime import date

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
        date_val = meta.get("date", "0000-00-00")

        entries.append({
            "date": date_val,
            "title": title,
            "path": path.relative_to("docs"),
            "ephemeral": False
        })

# -----------------------------
# ✅ 2. Load GROUPED EPHEMERAL job items
# -----------------------------

if ephemeral_path.exists():
    with open(ephemeral_path, encoding="utf-8") as f:
        ephemeral_items = json.load(f)

    for item in ephemeral_items:
        if item.get("type") == "job":
            sources = item.get("sources", [])

            if not sources:
                continue

            # ✅ Use the LATEST newsletter date for sorting
            latest_source = max(sources).replace(".md", "")

            entries.append({
                "date": latest_source,        # for sorting
                "title": item.get("title"),
                "sources": sources,           # ✅ REQUIRED for multi-date rendering
                "ephemeral": True
            })

# -----------------------------
# ✅ 3. Normalize & Sort ALL jobs together
# -----------------------------

def normalize_date(d):
    if isinstance(d, date):
        return d
    try:
        return date.fromisoformat(d)
    except Exception:
        return date(1900, 1, 1)

entries.sort(key=lambda x: normalize_date(x["date"]), reverse=True)

# -----------------------------
# ✅ 4. Write FINAL jobs.md
# -----------------------------

with mkdocs_gen_files.open("jobs.md", "w") as f:
    f.write("# 🧬 Job Opportunities\n\n")
    f.write("This page is generated automatically from permanent items and newsletters.\n\n---\n\n")

    for item in entries:
        if item["ephemeral"]:
            labels = [s.replace(".md", "") for s in item["sources"]]
            links = [f"[{lab}](newsletter/{lab}.md)" for lab in labels]
            joined = ", ".join(links)

            f.write(f"- {item['title']} (from newsletter) → {joined}\n")
        else:
            f.write(f"- [{item['title']}]({item['path']})\n")
