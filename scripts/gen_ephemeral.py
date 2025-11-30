from pathlib import Path
import re
import textwrap

NEWSLETTER_DIR = Path("docs/newsletter")

block_pattern = re.compile(
    r":::ephemeral\s*(.*?)\s*:::",
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
        data["__newsletter_file__"] = path.name
        ephemerals.append(data)


print("\n========== EPHEMERAL ITEMS FOUND ==========\n")

for e in ephemerals:
    print("Newsletter:", e["__newsletter_file__"])
    print("Type:", e.get("type"))
    print("Title:", e.get("title"))
    print("Tags:", e.get("tags"))
    print("Source:", e.get("source_newsletter"))
    print("Body:")
    print(textwrap.indent(e.get("body", ""), "  "))
    print("------------------------------------------")
