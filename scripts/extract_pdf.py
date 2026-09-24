"""Thin local MinerU 4.x batch adapter and checked extracted-bundle importer."""
import argparse
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

from validate_review import ROOT, asset_errors

ALLOWED = {".md", ".json", ".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}


def build_command(executable, pdf, output, tier):
    return [str(executable), "parse", str(pdf), "--output", str(output), "--format", "zip", "--pages", "all", "--tier", tier]


def probe(executable):
    executable = Path(executable).expanduser().resolve()
    if not executable.is_file():
        raise ValueError("existing mineru-kit executable not found; pass --mineru-kit")
    cli = executable.with_name("mineru")
    version = subprocess.run([str(cli), "--version"], capture_output=True, text=True, check=True, timeout=30).stdout.strip()
    if not re.search(r"\b4\.\d+", version):
        raise ValueError(f"unsupported MinerU interface: {version}; inspect and manually export")
    help_text = subprocess.run([str(executable), "parse", "--help"], capture_output=True, text=True, check=True, timeout=30).stdout
    for token in ("--output", "--format", "--pages", "--tier", "zip"):
        if token not in help_text:
            raise ValueError(f"MinerU capability probe missing {token}")
    return version


def import_extracted(markdown, destination):
    markdown = Path(markdown).expanduser()
    if markdown.is_symlink():
        raise ValueError("symlink Markdown is not a self-contained bundle")
    markdown = markdown.resolve()
    destination = Path(destination).resolve()
    if destination.is_relative_to(ROOT):
        raise ValueError("extraction must stay outside the Skill source tree")
    if destination.exists():
        raise FileExistsError("extracted output already exists; refusing overwrite")
    if not markdown.is_file() or markdown.suffix.lower() != ".md" or not markdown.read_text().strip():
        raise ValueError("nonempty MinerU Markdown required")
    files = []
    for path in markdown.parent.rglob("*"):
        if path.is_symlink():
            raise ValueError("symlink in extracted bundle")
        if path.is_file() and path.suffix.lower() in ALLOWED:
            if any(part.startswith(".") for part in path.relative_to(markdown.parent).parts):
                continue
            if path.suffix.lower() == ".md" and path != markdown:
                continue
            files.append(path)
    failures = asset_errors(markdown, markdown.parent)
    if failures:
        raise ValueError("invalid extracted assets: " + "; ".join(failures))
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".extract-", dir=destination.parent) as temp:
        pending = Path(temp) / "bundle"
        pending.mkdir()
        for path in files:
            relative = Path("paper.md") if path == markdown else path.relative_to(markdown.parent)
            target = pending / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        failures = asset_errors(pending / "paper.md", pending)
        if failures:
            raise ValueError("import omitted required asset: " + "; ".join(failures))
        pending.rename(destination)


def unpack_bundle(archive, destination):
    with zipfile.ZipFile(archive) as bundle:
        for entry in bundle.infolist():
            target = (destination / entry.filename).resolve()
            if not target.is_relative_to(destination.resolve()):
                raise ValueError("unsafe archive path")
            if (entry.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("archive symlink is not supported")
            if not entry.is_dir() and Path(entry.filename).suffix.lower() not in ALLOWED:
                raise ValueError(f"unexpected bundle file: {entry.filename}")
        bundle.extractall(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", nargs="?", type=Path)
    parser.add_argument("--mineru-kit", default=os.environ.get("MINERU_KIT") or shutil.which("mineru-kit"))
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--from-extracted", type=Path, metavar="PAPER_MD")
    parser.add_argument("--tier", choices=("basic", "standard", "advanced"), default="standard")
    args = parser.parse_args()
    try:
        if args.probe:
            if not args.mineru_kit:
                raise ValueError("pass the existing --mineru-kit executable")
            print(probe(args.mineru_kit))
            return
        if not args.workspace:
            raise ValueError("workspace required")
        workspace = args.workspace.expanduser().resolve()
        if workspace.is_relative_to(ROOT):
            raise ValueError("workspace must be outside the Skill source tree")
        if not (workspace / "source/paper.pdf").is_file():
            raise ValueError("initialize source/paper.pdf first")
        if (workspace / "extracted").exists():
            raise FileExistsError("extracted output exists; refusing overwrite")
        if args.from_extracted:
            import_extracted(args.from_extracted, workspace / "extracted")
        else:
            if not args.mineru_kit:
                raise ValueError("pass existing --mineru-kit; no parser is installed automatically")
            args.mineru_kit = Path(args.mineru_kit).expanduser().resolve()
            print(probe(args.mineru_kit))
            with tempfile.TemporaryDirectory(prefix=".mineru-", dir=workspace) as temp:
                temporary = Path(temp)
                archive = temporary / "paper.zip"
                subprocess.run(build_command(args.mineru_kit, workspace / "source/paper.pdf", archive, args.tier), check=True)
                unpacked = temporary / "unpacked"
                unpacked.mkdir()
                unpack_bundle(archive, unpacked)
                markdown = list(unpacked.rglob("*.md"))
                if len(markdown) != 1:
                    raise ValueError("expected exactly one Markdown export; inspect bundle")
                import_extracted(markdown[0], workspace / "extracted")
        print("Extraction imported. Inspect full text, figures and tables before review.")
    except (OSError, ValueError, subprocess.SubprocessError, zipfile.BadZipFile) as exc:
        parser.exit(1, f"ERROR: {exc}\n")


if __name__ == "__main__":
    main()
