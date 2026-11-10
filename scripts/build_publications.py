#!/usr/bin/env python3
"""Build Hugo publication data from one BibTeX file per paper folder.

Usage: python scripts/build_publications.py
Each content/publications/<slug>/ needs paper.bib and optionally metadata.yaml
and cover.{svg,png,jpg,jpeg,webp}. Generated artifacts are gitignored.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
import yaml

COVER_EXTS = ("webp", "png", "jpg", "jpeg", "svg")
REQUIRED = ("title", "author", "year")


class BibError(ValueError):
    pass


def parse_bibtex(text: str) -> tuple[str, str, dict[str, str]]:
    # Small parser for a single standard BibTeX record (nested braces supported).
    head = re.search(r"@\s*([A-Za-z]+)\s*[{(]\s*([^,\s]+)\s*,", text)
    if not head:
        raise BibError("Cannot find a BibTeX entry")
    if len(re.findall(r"@\s*[A-Za-z]+\s*[{(]", text)) != 1:
        raise BibError("Each paper.bib must contain exactly one BibTeX entry")
    kind, key = head.group(1).lower(), head.group(2)
    data: dict[str, str] = {}
    i, n = head.end(), len(text)
    while i < n:
        while i < n and text[i] in " \r\t\n,":
            i += 1
        if i >= n or text[i] in "})":
            break
        match = re.match(r"([A-Za-z_][A-Za-z0-9_-]*)\s*=\s*", text[i:])
        if not match:
            raise BibError(f"Malformed field near {text[i:i+40]!r}")
        field = match.group(1).lower()
        i += match.end()
        if i >= n:
            raise BibError(f"No value for {field}")
        if text[i] == "{":
            i += 1
            start, depth = i, 1
            while i < n and depth:
                if text[i] == "{" and (i == 0 or text[i - 1] != "\\"):
                    depth += 1
                elif text[i] == "}" and (i == 0 or text[i - 1] != "\\"):
                    depth -= 1
                i += 1
            if depth:
                raise BibError(f"Unbalanced braces in {field}")
            value = text[start:i - 1]
        elif text[i] == '"':
            i += 1
            start = i
            while i < n:
                if text[i] == '"' and text[i - 1] != "\\":
                    break
                i += 1
            if i >= n:
                raise BibError(f"Unterminated quoted value in {field}")
            value = text[start:i]
            i += 1
        else:
            start = i
            while i < n and text[i] not in ",\r\n})":
                i += 1
            value = text[start:i].strip()
        data[field] = value.strip()
    missing = [name for name in REQUIRED if not data.get(name)]
    if missing:
        raise BibError(f"Missing required fields: {', '.join(missing)}")
    return kind, key, data


def plain(text: str) -> str:
    # Remove BibTeX protective braces; retain ordinary visible text.
    return text.replace("{", "").replace("}", "").replace("\\&", "&").strip()


def generate(root: Path) -> list[dict]:
    input_dir = root / "content" / "publications"
    data_dir = root / "data"
    bib_dir = root / "static" / "bib"
    img_dir = root / "static" / "generated" / "publications"
    data_dir.mkdir(parents=True, exist_ok=True)
    bib_dir.mkdir(parents=True, exist_ok=True)
    img_dir.mkdir(parents=True, exist_ok=True)
    for p in bib_dir.glob("*.bib"):
        p.unlink()
    records: list[dict] = []
    keys: set[str] = set()
    all_bibs: list[str] = []
    for directory in sorted(input_dir.iterdir()):
        if not directory.is_dir() or not (directory / "paper.bib").exists():
            continue
        source = (directory / "paper.bib").read_text(encoding="utf-8").strip() + "\n"
        try:
            kind, key, fields = parse_bibtex(source)
            metadata_path = directory / "metadata.yaml"
            meta = yaml.safe_load(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
            meta = meta or {}
            if not isinstance(meta, dict):
                raise ValueError("metadata.yaml must contain a mapping")
            if key in keys:
                raise BibError(f"Duplicate citation key: {key}")
            if not re.fullmatch(r"[A-Za-z0-9_.:-]+", key):
                raise BibError(f"Unsupported BibTeX key for URL: {key}")
            keys.add(key)
            if not re.fullmatch(r"\d{4}", plain(fields["year"])):
                raise BibError("year must be a four-digit number")
            cover_url = ""
            for ext in COVER_EXTS:
                cover = directory / f"cover.{ext}"
                if cover.is_file():
                    target = img_dir / directory.name
                    target.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(cover, target / cover.name)
                    cover_url = f"/generated/publications/{directory.name}/{cover.name}"
                    break
            links = meta.get("links") or {}
            if not isinstance(links, dict):
                raise ValueError("metadata.links must be a mapping")
            paper_url = links.get("paper") or fields.get("url") or (
                f"https://doi.org/{plain(fields['doi'])}" if fields.get("doi") else ""
            )
            record = {
                "slug": directory.name,
                "type": kind,
                "citation_key": key,
                "title": plain(fields["title"]),
                "authors": plain(fields["author"]).replace(" and ", ", "),
                "year": int(plain(fields["year"])),
                "venue": meta.get("venue") or plain(fields.get("booktitle") or fields.get("journal") or "Preprint"),
                "status": meta.get("status") or "Publication",
                "label": meta.get("label") or "",
                "summary": meta.get("summary") or "",
                "details": meta.get("details") or "",
                "featured": bool(meta.get("featured", False)),
                "order": int(meta.get("order", 9999)),
                "cover": cover_url,
                "paper_url": paper_url,
                "doi_url": links.get("doi") or (f"https://doi.org/{plain(fields['doi'])}" if fields.get("doi") else ""),
                "code_url": links.get("code") or "",
                "slides_url": links.get("slides") or "",
                "project_url": links.get("project") or "",
                "bib_url": f"/bib/{key}.bib",
            }
            records.append(record)
            all_bibs.append(source.rstrip())
            (bib_dir / f"{key}.bib").write_text(source, encoding="utf-8")
        except (ValueError, TypeError) as e:
            raise SystemExit(f"Error processing {directory}: {e}") from e
    records.sort(key=lambda p: (-p["year"], p["title"].lower()))
    (data_dir / "publications.json").write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (root / "static" / "publications.bib").write_text("\n\n".join(all_bibs) + "\n", encoding="utf-8")
    print(f"Generated {len(records)} publications and consolidated BibTeX.")
    return records


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    generate(args.project_root.resolve())
