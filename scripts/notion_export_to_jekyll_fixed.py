#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import datetime as dt
import io
import os
import re
import sys
import zipfile
from pathlib import Path

# ---------- Helpers ----------

def parse_date(value: str) -> str | None:
    """Notion export often uses 'December 25, 2025'. Convert to YYYY-MM-DD."""
    if not value or value.strip() == "":
        return None
    value = value.strip()
    # Try common formats
    for fmt in ("%B %d, %Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return dt.datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    # If unknown, return raw (better than crashing)
    return value

def slugify_section(section: str) -> str:
    return section.strip().lower().replace(" ", "-")

def split_tags(value: str) -> list[str]:
    if not value or value.strip() == "":
        return []
    # Notion export uses "A, B, C"
    return [t.strip() for t in value.split(",") if t.strip()]

def extract_ai_names(value: str) -> list[str]:
    """
    Notion relation export looks like:
    'Claude Sonnet 4.5 (https://... ), ChatGPT (https://...)'
    We'll extract names before each '(http...)'.
    """
    if not value or value.strip() == "":
        return []
    
    # Strategy: split by ), then for each part take what's before (
    parts = value.split(')')
    names = []
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # If there's a (, take everything before it
        if '(' in part:
            name = part.split('(')[0].strip()
            # Remove any leading/trailing comma
            name = name.strip(',').strip()
            if name:
                names.append(name)
    
    # Fallback: if no matches, try comma split
    if not names:
        names = split_tags(value)
    
    return names

def yaml_quote(s: str) -> str:
    s = s.replace('"', '\\"')
    return f"\"{s}\""

def yaml_list(key: str, items: list[str]) -> str:
    if not items:
        return ""
    out = [f"{key}:"]
    for it in items:
        out.append(f"  - {it}")
    return "\n".join(out)

def clean_notion_md(md_text: str) -> str:
    """
    Notion MD export often:
    - Starts with '# Title'
    - Then property lines 'Key: Value'
    - Then a fenced code block ```markdown ... ```
    We remove the heading + property block and unwrap the markdown fence if present.
    """
    text = md_text.replace("\r\n", "\n")

    # If there is a ```markdown fenced block, unwrap it (keep inner content)
    m = re.search(r"```markdown\s*\n(.*?)\n```", text, flags=re.DOTALL)
    if m:
        inner = m.group(1).strip("\n")
        return inner.strip() + "\n"

    # Otherwise: remove first H1 line and following "Key: Value" lines until blank line
    lines = text.split("\n")
    i = 0
    if i < len(lines) and lines[i].startswith("# "):
        i += 1
    # skip empty lines
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    # skip property-like lines
    while i < len(lines) and re.match(r"^[A-Za-z0-9 _-]+:\s", lines[i]):
        i += 1
    # skip following empty lines
    while i < len(lines) and lines[i].strip() == "":
        i += 1

    body = "\n".join(lines[i:]).strip() + "\n"
    return body

# ---------- Zip reading ----------

def open_nested_zip(path: Path) -> zipfile.ZipFile:
    """
    Your export is a zip that contains another zip (ExportBlock-...-Part-1.zip).
    This returns the INNER zip handle.
    """
    outer = zipfile.ZipFile(path)
    inner_names = [n for n in outer.namelist() if n.lower().endswith(".zip")]
    if not inner_names:
        return outer  # already flat
    inner_data = outer.read(inner_names[0])
    return zipfile.ZipFile(io.BytesIO(inner_data))

def read_csv_from_zip(z: zipfile.ZipFile, csv_name: str) -> list[dict]:
    raw = z.read(csv_name)
    text = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    return list(reader)

def find_content_csv(z: zipfile.ZipFile) -> str:
    # Prefer *_all.csv if present
    candidates = [n for n in z.namelist() if n.lower().endswith(".csv") and "/content " in n.lower()]
    if not candidates:
        raise FileNotFoundError("No CONTENT CSV found in the zip.")
    all_csv = [c for c in candidates if c.lower().endswith("_all.csv")]
    return all_csv[0] if all_csv else candidates[0]

def find_content_md_files(z: zipfile.ZipFile) -> list[str]:
    return [n for n in z.namelist() if n.lower().endswith(".md") and "/content/" in n.lower()]

def match_row_by_title(rows: list[dict], title: str) -> dict | None:
    for r in rows:
        if (r.get("Title") or "").strip() == title.strip():
            return r
    return None

# ---------- Output mapping ----------

def output_path_for(row: dict, out_dir: Path) -> Path:
    section = (row.get("Section") or "").strip()
    slug = (row.get("Slug") or "").strip()
    date = parse_date(row.get("Date") or "")
    
    # Mappa Section Notion → Collection Jekyll
    section_map = {
        "OB-Session": "_ob-session",
        "OB-Progetti": "_ob-progetti",
        "OB-AI": "_ob-ai",
        "OB-Archives": "_ob-archivio",
        "OB-Archivio": "_ob-archivio",
    }
    
    folder = section_map.get(section, "_pages")
    
    # Filename con data per sort cronologico
    if date:
        filename = f"{date}-{slug}.md"
    else:
        filename = f"{slug or 'untitled'}.md"
    
    return out_dir / folder / filename
def build_front_matter(row: dict) -> str:
    title = (row.get("Title") or "").strip()
    slug = (row.get("Slug") or "").strip()
    section = (row.get("Section") or "").strip()
    subsection = (row.get("Subsection") or "").strip()
    layout = (row.get("Layout") or "").strip()
    type_ = (row.get("Type") or "").strip()
    status = (row.get("Status") or "").strip().lower()
    date = parse_date(row.get("Date") or "")
    tags = split_tags(row.get("Tags") or "")
    ai = extract_ai_names(row.get("AI Models") or row.get("AI Partecipanti") or "")
    description = (row.get("Meta Description") or "").strip()
    meta_title = (row.get("Meta Title") or row.get("meta-title") or row.get("meta_title") or "").strip()
    keywords = (row.get("Keywords SEO") or "").strip()

    lines = ["---"]
    if title: lines.append(f"title: {yaml_quote(title)}")
    if slug: lines.append(f"slug: {yaml_quote(slug)}")
    if layout: lines.append(f"layout: {layout}")
    if section: lines.append(f"section: {section}")
    if subsection and subsection.lower() != "nan": lines.append(f"subsection: {subsection}")
    if type_: lines.append(f"type: {type_}")
    if date: lines.append(f"date: {date}")
    if description: lines.append(f"description: {yaml_quote(description)}")
    if meta_title: lines.append(f"meta_title: {yaml_quote(meta_title)}")
    if keywords: lines.append(f"keywords: {yaml_quote(keywords)}")

    tags_block = yaml_list("tags", tags)
    if tags_block:
        lines.append(tags_block)

    ai_block = yaml_list("ai", ai)
    if ai_block:
        lines.append(ai_block)

    # Draft handling: keep file but mark as unpublished
    if status and status not in ("published", "pubblicato"):
        lines.append("published: false")

    lines.append("---")
    return "\n".join(lines) + "\n"

# ---------- Main ----------

def main():
    ap = argparse.ArgumentParser(description="Convert Notion CONTENT export zip to Jekyll-friendly Markdown.")
    ap.add_argument("zip", help="Path to Notion export zip")
    ap.add_argument("--out", default=".", help="Output directory (repo root). Default: current dir")
    args = ap.parse_args()

    zip_path = Path(args.zip).expanduser().resolve()
    out_dir = Path(args.out).expanduser().resolve()

    z = open_nested_zip(zip_path)

    content_csv_name = find_content_csv(z)
    rows = read_csv_from_zip(z, content_csv_name)

    md_files = find_content_md_files(z)
    if not md_files:
        print("No CONTENT markdown files found.", file=sys.stderr)
        sys.exit(1)

    generated = 0
    for md_name in md_files:
        md_text = z.read(md_name).decode("utf-8-sig", errors="replace")

        # Title is first line "# Title"
        first_line = md_text.split("\n", 1)[0].strip()
        title = first_line[2:].strip() if first_line.startswith("# ") else ""

        row = match_row_by_title(rows, title) if title else None
        if not row:
            # fallback: skip if can't match
            print(f"Skipping (no CSV row match): {md_name}", file=sys.stderr)
            continue

        fm = build_front_matter(row)
        body = clean_notion_md(md_text)

        out_path = output_path_for(row, out_dir)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        out_path.write_text(fm + "\n" + body, encoding="utf-8")
        generated += 1
        print(f"Wrote: {out_path}")

    print(f"\nDone. Generated {generated} file(s).")

if __name__ == "__main__":
    main()
