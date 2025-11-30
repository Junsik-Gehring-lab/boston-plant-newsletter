from pathlib import Path
import yaml
import json
import mkdocs_gen_files
from datetime import date

items_dir = Path("docs/items/grants")
ephemeral_path = Path("docs/.cache/ephemeral.json")

entries = []

# -----------------------------
# ✅ 1. Load PERMANENT grants
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
# ✅ 2. Load EPHEMERAL grants
# -----------------------------

if ephemeral_path.exists():
    with open(ephemeral_path, encoding="utf-8") as f:
        ephemeral_items = json.load(f)

    for item in ephemeral_items:
        if item.get("type") == "grant":
            entries.append({
                "date": item.get("source_newsletter", "0000-00-00"),
                "title": item.get("title"),
                "path": f"newsletter/{item.get('source_file')}",
                "ephemeral": True
            })

# -----------------------------
# ✅ 3. Normalize & sort dates
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
# ✅ 4. Write FINAL grants.md
# -----------------------------

with mkdocs_gen_files.open("grants.md", "w") as f:
    f.write("# 💰 Grants & Fellowships\n\n")
    f.write("This page is generated automatically from permanent items and newsletters.\n\n---\n\n")

    for item in entries:
        if item["ephemeral"]:
            f.write(f"- 📰 **{item['title']}** *(from newsletter)* → [{item['path']}]({item['path']})\n")
        else:
            f.write(f"- [{item['title']}]({item['path']})\n")
