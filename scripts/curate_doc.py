"""Add or update documentation in collection directories.

Routes each source URL to a direct markdown fetch (`markdown_source`, for any
`.md` URL — GitHub included) or a FireCrawl scrape, derives a filename from the
URL path, and updates INDEX.xml. Filenames are stable across re-scrapes.
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import firecrawl_source
import markdown_source


def _normalise_directory_path(dir_path_str: str) -> Path:
    """Normalise directory path by removing trailing slash."""
    return Path(dir_path_str.rstrip("/"))


def _format_path_for_display(path: Path) -> str:
    """Format path as a project-relative string, e.g. `vite/INDEX.xml`.

    Falls back to `str(path)` for paths outside the project root.
    """
    try:
        absolute_path = path.resolve()
        project_root = Path.cwd()
        return str(absolute_path.relative_to(project_root))
    except ValueError:
        # Path is outside project (edge case) - return as-is
        return str(path)


def _validate_url(url: str) -> None:
    """Validate URL has scheme and netloc, exit if invalid."""
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        print(f"❌ Error: INVALID_URL|{url}|")
        sys.exit(1)


def _reject_uv_docs_url(url: str) -> None:
    """Reject hosted-docs uv URLs; the uv collection is sourced from GitHub."""
    if url.startswith("https://docs.astral.sh/uv/"):
        print(
            "❌ Error: USE_GITHUB_BLOB|"
            "Use the GitHub blob URL for this source; "
            "see uv/INDEX.xml for the canonical mapping|"
            f"{url}|"
        )
        sys.exit(1)


def _validate_directory_for_collection(dir_path: Path, index_path: Path) -> None:
    """Exit if directory exists, is non-empty, and lacks INDEX.xml.

    Prevents overwriting unrelated files in a non-collection directory.
    """
    if dir_path.exists() and not index_path.exists() and any(dir_path.iterdir()):
        print(
            f"❌ Error: INVALID_COLLECTION|"
            f"Directory non-empty and missing INDEX.xml. "
            f"Rejected to prevent inadvertent file overwrites|{dir_path}|"
        )
        sys.exit(1)


def filename_from_url(url: str) -> str:
    """Derive a `.md` filename from a (non-GitHub) doc URL path.

    Drops everything up to and including a `docs` path segment, strips a
    trailing `.md`, then lowercases and sanitises the remainder into a
    hyphen-joined slug. A bare docs root falls back to `index.md`.
    """
    segments = [s for s in urlparse(url).path.strip("/").split("/") if s]
    if segments and segments[-1].endswith(".md"):
        segments[-1] = segments[-1][:-3]
    if "docs" in segments:
        segments = segments[segments.index("docs") + 1 :]
    slug = re.sub(r"[^a-z0-9]+", "-", "-".join(segments).lower()).strip("-")
    return f"{slug or 'index'}.md"


def _create_readme(dir_path: Path, source_site_url: str) -> None:
    """Create README.md for new collection with overview and source link."""
    readme_content = f"""# {dir_path.name} Documentation

Curated docs for targeted AI context.

- Curation Index: [INDEX.xml](INDEX.xml)
- Curation Source: <{source_site_url}>
"""
    readme_path = dir_path / "README.md"
    readme_path.write_text(readme_content)
    print(f"✅ Created curation readme|{_format_path_for_display(readme_path)}|")


def _create_index_xml(dir_path: Path) -> None:
    """Create empty INDEX.xml structure."""
    root = ET.Element("docs_index")
    ET.indent(root, space="  ")

    tree = ET.ElementTree(root)
    index_path = dir_path / "INDEX.xml"
    tree.write(index_path, encoding="unicode", xml_declaration=False)
    print(f"✅ Created curation index|{_format_path_for_display(index_path)}|")


def _add_or_update_source_in_index(
    dir_path: Path, title: str, source_url: str, local_file: str
) -> bool:
    """Add or replace the source for `source_url` in INDEX.xml.

    Returns `is_update` — True if an existing entry was replaced.
    """
    index_path = dir_path / "INDEX.xml"

    tree = ET.parse(index_path)
    root = tree.getroot()

    is_update = False

    for existing_source in root.findall("source"):
        existing_url_elem = existing_source.find("source_url")
        if (
            existing_url_elem is not None
            and existing_url_elem.text is not None
            and existing_url_elem.text.rstrip("/") == source_url
        ):
            root.remove(existing_source)
            is_update = True
            break

    source = ET.SubElement(root, "source")
    ET.SubElement(source, "title").text = title
    ET.SubElement(source, "description").text = "PLACEHOLDER"
    ET.SubElement(source, "source_url").text = source_url
    ET.SubElement(source, "local_file").text = local_file
    ET.SubElement(source, "scraped_at").text = date.today().isoformat()

    ET.indent(root, space="  ")

    tree.write(index_path, encoding="unicode", xml_declaration=False)

    if is_update:
        print(f"✅ Updated index source|{_format_path_for_display(index_path)}|")
    else:
        print(f"✅ Added index source|{_format_path_for_display(index_path)}|")

    print("💡 INDEX.xml <description> pending: PLACEHOLDER requires summary|")

    return is_update


def main() -> None:
    """Add or update documentation in a collection directory.

    Workflow:
        1. Validate URL and directory
        2. Route: direct fetch for `.md` URLs (GitHub or any other), else FireCrawl
        3. Create collection structure if new (README.md, INDEX.xml)
        4. Write the markdown file (overwriting any existing one) and add or
           update the INDEX.xml entry keyed by source URL

    Filenames are derived from the URL path, so they stay stable across
    re-scrapes even when the upstream title changes.
    """
    parser = argparse.ArgumentParser(
        description="Add or update documentation in a collection directory"
    )

    parser.add_argument(
        "directory",
        help="Documentation directory (e.g. `tailwind/`)",
    )
    parser.add_argument(
        "source_url",
        help="Web URL to curate (direct `.md` fetch or FireCrawl scrape)",
    )

    args = parser.parse_args()

    source_url: str = args.source_url.rstrip("/")  # canonical form: no trailing slash
    dir_path = _normalise_directory_path(args.directory)
    index_path = dir_path / "INDEX.xml"

    _validate_url(source_url)
    _reject_uv_docs_url(source_url)
    _validate_directory_for_collection(dir_path, index_path)

    print(f"✅ Starting to curate from|{source_url}|")

    dir_path.mkdir(parents=True, exist_ok=True)

    # Route before creating files (fail fast). GitHub is checked first: a blob
    # URL also ends in `.md`, but it is stored as blob and fetched from raw.
    if markdown_source.is_github_url(source_url):
        # Exits unless this is a main/master blob .md URL; raw_url is the fetch target.
        raw_url = markdown_source.github_blob_to_raw_url(source_url)
        print(f"✅ Detected GitHub source|{source_url}|")
        candidate = markdown_source.github_filename_from_blob_url(source_url)
        content = markdown_source.fetch_markdown(raw_url)  # exits on 404/network
        title = markdown_source.extract_title(content, raw_url)
        # source_url stays the BLOB URL → stored verbatim in INDEX.xml
    elif markdown_source.is_md_url(source_url):
        candidate = filename_from_url(source_url)
        content = markdown_source.fetch_markdown(source_url)  # exits on 404/network
        title = markdown_source.extract_title(content, source_url)
    else:
        content, title = firecrawl_source.scrape(source_url)
        candidate = filename_from_url(source_url)

    # scheme + netloc for the README's curation-source link
    parsed_url = urlparse(source_url)
    source_site_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    if not index_path.exists():
        _create_readme(dir_path, source_site_url)
        _create_index_xml(dir_path)

    # Filename is derived from the URL path
    filename = candidate
    file_path = dir_path / filename

    file_existed = file_path.exists()
    file_path.write_text(content)
    if file_existed:
        print(f"✅ Overwrote existing document|{_format_path_for_display(file_path)}|")
    else:
        print(f"✅ Created new document|{_format_path_for_display(file_path)}|")

    is_update = _add_or_update_source_in_index(dir_path, title, source_url, filename)

    # source_url is canonical (blob form for GitHub, rstripped user URL otherwise)
    verb = "overwrote and re-indexed" if is_update else "created and indexed new"
    print(f"🎉 Curation Success!|{verb} document|{source_url}|\n")


if __name__ == "__main__":
    main()
