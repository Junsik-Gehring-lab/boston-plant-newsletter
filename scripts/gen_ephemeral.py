from pathlib import Path
import re
import textwrap
import json

NEWSLETTER_DIR = Path("docs/newsletter")
OUTPUT_DIR = Path("docs/.cache")
OUTPUT_PATH = OUTPUT_DIR / "ephemeral.json"

block_pattern = re.compile(
    r"<!--\s*:::ephemeral\s*(.*?)\s*:::\s*-->",
    re.DOTALL
)


keyval_pattern = re.compile(r"^([a-zA-Z_]+):\s*(.+)$")

def parse_block(raw):
    lines = raw.strip().splitlines()
    meta = {}
    body = []

    for line in lines:
        m = keyval_pattern.match(line)
        if m:
            key, val = m.groups()
            meta[key.strip()] = val.strip()
        else:
            body.append(line)

    meta["body"] = "\n".join(body).strip()
    return meta


ephemerals = []

for path in NEWSLETTER_DIR.glob("*.md"):
    text = path.read_text(encoding="utf-8")
    blocks = block_pattern.findall(text)

    for raw in blocks:
        data = parse_block(raw)

        # ✅ Normalize fields for downstream generators
        data["source_file"] = path.name   # REQUIRED by gen_jobs.py

        # ✅ Normalize tags into a list
        if "tags" in data:
            data["tags"] = [t.strip() for t in data["tags"].split(",") if t.strip()]
        else:
            data["tags"] = []

        ephemerals.append(data)

# -----------------------------
# ✅ GROUP BY (type + title)
# -----------------------------

grouped = {}

for item in ephemerals:
    key = (item.get("type"), item.get("title"))

    if key not in grouped:
        grouped[key] = {
            "type": item.get("type"),
            "title": item.get("title"),
            "tags": item.get("tags", []),
            "sources": [item.get("source_file")],  # ✅ LIST now
        }
    else:
        grouped[key]["sources"].append(item.get("source_file"))

final_items = list(grouped.values())

# -----------------------------
# ✅ WRITE TO DISK
# -----------------------------

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(final_items, f, indent=2, ensure_ascii=False)

print(f"\n✅ Wrote {len(final_items)} grouped ephemeral items to {OUTPUT_PATH}\n")

# -----------------------------
# ✅ DEBUG PRINTOUT (KEEP THIS)
# -----------------------------

print("\n========== EPHEMERAL ITEMS FOUND ==========\n")

for e in ephemerals:
    print("Newsletter:", e.get("source_file"))
    print("Type:", e.get("type"))
    print("Title:", e.get("title"))
    print("Tags:", e.get("tags"))
    print("Source:", e.get("source_newsletter"))
    print("Body:")
    print(textwrap.indent(e.get("body", ""), "  "))
    print("------------------------------------------")
