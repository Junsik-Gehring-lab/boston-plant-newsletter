from pathlib import Path
import yaml
import json
import mkdocs_gen_files
from collections import defaultdict

# -----------------------------
# ✅ 1. Permanent item sources
# -----------------------------

item_dirs = [
    Path("docs/items/grants"),
    Path("docs/items/jobs"),
    Path("docs/items/seminars"),
    Path("docs/items/organizations")
]

# -----------------------------
# ✅ 2. Ephemeral cache source
# -----------------------------

ephemeral_path = Path("docs/.cache/ephemeral.json")

tags = defaultdict(list)

# -----------------------------
# ✅ 3. Load PERMANENT items
# -----------------------------

for item_dir in item_dirs:
    for path in item_dir.glob("*.md"):
        text = path.read_text()
        if not text.startswith("---"):
            continue

        meta = yaml.safe_load(text.split("---", 2)[1])
        title = meta.get("title", path.stem)
        item_tags = meta.get("tags", [])

        rel_path = "../" + str(path.relative_to("docs")).replace("\\", "/")

        for tag in item_tags:
            tags[tag].append({
                "title": title,
                "path": rel_path,
                "ephemeral": False
            })

# -----------------------------
# ✅ 4. Load GROUPED EPHEMERAL items
# -----------------------------

if ephemeral_path.exists():
    with open(ephemeral_path, encoding="utf-8") as f:
        ephemeral_items = json.load(f)

    for item in ephemeral_items:
        title = item.get("title")
        item_tags = item.get("tags", [])
        sources = item.get("sources", [])

        if not title or not item_tags or not sources:
            continue

        for tag in item_tags:
            tags[tag].append({
                "title": title,
                "sources": sources,   # ✅ LIST of newsletter files
                "ephemeral": True
            })

# -----------------------------
# ✅ 5. Generate main tag index
# -----------------------------

with mkdocs_gen_files.open("tags.md", "w") as f:
    f.write("# 🏷️ Browse by Tag\n\n")
    f.write("Click any tag to view all related items.\n\n---\n\n")

    for tag in sorted(tags):
        f.write(f"- [{tag}](tags/{tag}.md) ({len(tags[tag])})\n")

# -----------------------------
# ✅ 6. Generate one page per tag
# -----------------------------

for tag, items in tags.items():
    with mkdocs_gen_files.open(f"tags/{tag}.md", "w") as f:
        f.write(f"# 🏷️ Tag: {tag}\n\n")
        f.write("Items with this tag:\n\n---\n\n")

        for item in items:
            if item["ephemeral"]:
                # ✅ Multi-date rendering from grouped sources
                labels = [s.replace(".md", "") for s in item["sources"]]
                links = [f"[{lab}](../newsletter/{lab}.md)" for lab in labels]
                joined = ", ".join(links)

                f.write(f"- {item['title']} (from newsletter) → {joined}\n")
            else:
                f.write(f"- [{item['title']}]({item['path']})\n")
