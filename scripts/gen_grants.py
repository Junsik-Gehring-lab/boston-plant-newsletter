from pathlib import Path
import yaml
import mkdocs_gen_files

items_dir = Path("docs/items/grants")

entries = []

for path in sorted(items_dir.glob("*.md")):
    text = path.read_text()
    if text.startswith("---"):
        meta = yaml.safe_load(text.split("---", 2)[1])
        title = meta.get("title", path.stem)
        date = meta.get("date", "0000-00-00")
        entries.append((date, title, path))

entries.sort(reverse=True)

with mkdocs_gen_files.open("grants.md", "w") as f:
    f.write("# 💰 Grants & Fellowships\n\n")
    f.write("This page is generated automatically from `docs/items/grants/`.\n\n---\n\n")
    for date, title, path in entries:
        f.write(f"- [{title}]({path.relative_to('docs')})\n")
