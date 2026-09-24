"""Initialize one review outside the Skill tree; never overwrite existing work."""
import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def initialize(pdf, destination):
    pdf = Path(pdf).expanduser().resolve()
    destination = Path(destination).expanduser().resolve()
    if not pdf.is_file() or pdf.suffix.lower() != ".pdf":
        raise ValueError("input must be an existing PDF")
    if destination.is_relative_to(ROOT):
        raise ValueError("review workspace must be outside the Skill source tree")
    if destination.exists():
        raise FileExistsError("destination already exists; refusing overwrite")
    destination.mkdir(parents=True)
    for name in ("source", "review", "output"):
        (destination / name).mkdir()
    shutil.copy2(pdf, destination / "source/paper.pdf")
    shutil.copy2(ROOT / "templates/paper-review.md", destination / "review/paper-review.md")
    manifest = yaml.safe_load((ROOT / "templates/manifest.yaml").read_text())
    manifest["review"]["generated_at"] = datetime.now(timezone.utc).isoformat()
    (destination / "review/manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True))
    # Blog creation is deliberately deferred until the review gate passes.
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("workspace", type=Path)
    args = parser.parse_args()
    try:
        print(initialize(args.pdf, args.workspace))
    except (ValueError, OSError) as exc:
        parser.exit(1, f"ERROR: {exc}\n")


if __name__ == "__main__":
    main()
