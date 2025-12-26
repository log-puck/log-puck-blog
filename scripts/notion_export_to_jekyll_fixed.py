from pathlib import Path
from datetime import datetime


def parse_date(value: str) -> str:
    """Parse a date string into YYYY-MM-DD format or return an empty string."""
    value = (value or "").strip()
    if not value:
        return ""

    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    return ""


def output_path_for(row: dict, out_dir: Path) -> Path:
    section = (row.get("Section") or "").strip()
    slug = (row.get("Slug") or "").strip()
    date = parse_date(row.get("Date") or "")

    # Normalizzazione deterministica
    section_key = section.lower()
    slug = slug or "untitled"

    # Mappa Section Notion → Folder collection Jekyll
    section_map = {
        "ob-session": "_ob-session",
        "ob-progetti": "_ob-progetti",
        "ob-ai": "_ob-ai",
        "ob-archives": "_ob-archivio",
        "ob-archivio": "_ob-archivio",
    }

    folder = section_map.get(section_key, "_pages")

    # Filename: con data per sort cronologico
    filename = f"{date}-{slug}.md" if date else f"{slug}.md"
    return out_dir / folder / filename
