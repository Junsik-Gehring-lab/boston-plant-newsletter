from pathlib import Path
import mkdocs_gen_files

newsletter_dir = Path("docs/newsletter")

entries = []

for path in newsletter_dir.glob("*.md"):
    if path.name.lower() == "index.md":
        continue
    date = path.stem  # expects filenames like 2025-02-07.md
    entries.append((date, path))

entries.sort(reverse=True)

with mkdocs_gen_files.open("newsletter.md", "w") as f:
    f.write("# 🗞️ Newsletter Archive\n\n")
    f.write("All past issues of the Regional Science Newsletter.\n\n---\n\n")

    current_year = None
    
    for date, path in entries:
        year = date.split("-")[0]
        if year != current_year:
            f.write(f"\n## {year}\n\n")
            current_year = year
        
        f.write(f"- [{date} Issue]({path.relative_to('docs')})\n")
