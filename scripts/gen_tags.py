from pathlib import Path
import yaml
import mkdocs_gen_files
from collections import defaultdict

item_dirs = [
    Path("docs/items/grants"),
    Path("docs/items/jobs"),
    Path("docs/items/seminars"),
]

tags = defaultdict(list)

for item_dir in item_dirs:
    for path in item_dir.glob("*.md"):
        text = path.read_text()
        if not text.startswith("---"):
            continue

        meta = yaml.safe_load(text.split("---", 2)[1])
        title = meta.get("title", path.stem)
        item_tags = meta.get("tags", [])

        # ✅ FORCE ROOT-RELATIVE PATH
        rel_path = "/" + str(path.relative_to("docs")).replace("\\", "/")

        for tag in item_tags:
            tags[tag].append((title, rel_path))

# ✅ Generate main tag index
with mkdocs_gen_files.open("tags.md", "w") as f:
    f.write("# 🏷️ Browse by Tag\n\n")
    f.write("Click any tag to view all related items.\n\n---\n\n")

    for tag in sorted(tags):
        f.write(f"- [{tag}](tags/{tag}.md) ({len(tags[tag])})\n")

# ✅ Generate one page per tag
for tag, items in tags.items():
    with mkdocs_gen_files.open(f"tags/{tag}.md", "w") as f:
        f.write(f"# 🏷️ Tag: {tag}\n\n")
        f.write("Items with this tag:\n\n---\n\n")

        for title, rel_path in items:
            f.write(f"- [{title}]({rel_path})\n")
