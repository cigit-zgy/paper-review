"""Deterministic artifact checks; no scientific quality scoring or model calls."""
import argparse
import json
import re
from datetime import date, datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = (
    "Paper identity", "One-sentence contribution", "Research question",
    "Scientific motivation", "Method architecture", "Data and experimental design",
    "Main findings", "Claimed innovations", "Figures and tables", "Limitations",
    "Reproducibility", "Transferability", "Critical assessment",
)
BLOG_SECTIONS = (
    "这篇论文解决什么问题？", "研究思路是什么？", "作者真正证明了什么？",
    "创新点在哪里？", "哪些结论证据仍然不足？", "这项工作有哪些局限？",
    "对我的研究有什么可迁移价值？", "参考文献",
)
ANALYSIS_FIELDS = (
    "role", "question", "what_is_shown", "variables_axes_groups", "comparison",
    "main_observation", "authors_interpretation", "evidence_strength", "limitations",
)
INNOVATION_FIELDS = (
    "Author claim", "Prior approach / comparison target", "What actually changed",
    "Supporting evidence", "Reviewer assessment", "Transferability",
)
OBJECT_REF = re.compile(r"\b(Figure|Fig\.?|Table)\s+(S?[1-9][0-9]*)([a-z])?\b", re.I)
HAN = re.compile(r"[\u3400-\u9fff]")


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently discarding evidence."""


def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, (str, int, float, bool, type(None))):
            raise ValueError("manifest keys must be scalar")
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_yaml(text):
    return yaml.load(text, Loader=UniqueLoader)


def normalized(text):
    return " ".join(text.split())


def prose(text):
    text = re.sub(r"```.*?```|~~~.*?~~~", "", text, flags=re.S)
    return re.sub(r"<!--.*?-->|\{/\*.*?\*/\}", "", text, flags=re.S)


def object_refs(text):
    result = []
    for kind, number, panel in OBJECT_REF.findall(text):
        kind = "Table" if kind.lower() == "table" else "Figure"
        result.append((f"{kind} {number.upper()}", panel.lower()))
    return result


def safe_file(root, value, base=None):
    path = Path(value)
    if path.is_absolute():
        raise ValueError(f"absolute local asset/source path: {value}")
    path = ((base or root) / path).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"path outside workspace: {value}")
    if not path.is_file():
        raise ValueError(f"missing asset/source: {value}")
    return path


def asset_errors(path, root):
    """Check static Markdown/HTML links and local MDX imports; reject dynamic src."""
    text = prose(path.read_text(encoding="utf-8"))
    values = re.findall(r'(?<![\w:-])(?:src|href)\s*=\s*["\']([^"\']+)["\']', text)
    for raw in re.findall(r"!?\[[^\]]*\]\(([^\n]*?)\)", text):
        if raw.startswith("<") and ">" in raw:
            values.append(raw[1:raw.index(">")])
        else:
            values.append(re.split(r'\s+["\']', raw, maxsplit=1)[0])
    values.extend(re.findall(r'^\[[^\]]+\]:\s*<?([^>\n]+)>?$', text, re.M))
    values.extend(re.findall(r'import\s+.+?\s+from\s+["\']([^"\']+)["\']', text))
    errors = []
    if re.search(r"(?<![\w:-])src\s*=\s*\{", text):
        errors.append(f"{path.name}: dynamic src unsupported; use a checked static path")
    for value in values:
        value = value.strip()
        if value.startswith(("#", "@/components/")):
            continue
        parsed = urlsplit(value)
        if parsed.scheme in {"https", "http", "mailto"}:
            continue
        if parsed.scheme or parsed.netloc:
            errors.append(f"unsupported asset/link scheme: {value}")
            continue
        try:
            safe_file(root, unquote(parsed.path), path.parent)
        except ValueError as exc:
            errors.append(str(exc))
    return errors


def heading_blocks(text, level):
    pattern = re.compile(r"^" + "#" * level + r" (.+?)\s*$", re.M)
    matches = list(pattern.finditer(text))
    return [(m[1], text[m.end(): matches[i + 1].start() if i + 1 < len(matches) else len(text)]) for i, m in enumerate(matches)]


def validate(workspace, stage="blog"):
    root = Path(workspace).resolve()
    errors = []
    try:
        data = load_yaml((root / "review/manifest.yaml").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas/paper-review.schema.json").read_text())
        failures = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data))
        if failures:
            return [f"manifest {'.'.join(map(str, e.absolute_path))}: {e.message}" for e in failures]
    except (OSError, ValueError, yaml.YAMLError, RecursionError) as exc:
        return [f"manifest: {exc}"]
    review = data["review"]
    for key in ("full_text_read", "inventory_checked"):
        if not review[key]:
            errors.append(f"review.{key} must be true after source inspection")
    if review["status"] != "reviewed" or not review["coverage"]:
        errors.append("review must be reviewed with explicit full-text coverage")
    if any(item["blocks_blog"] for item in review["uncertainties"]):
        errors.append("unresolved extraction uncertainty blocks blog generation")
    source = ""
    for key, value in data["source"].items():
        try:
            file = safe_file(root, value)
            if key == "extracted_markdown":
                source = file.read_text(encoding="utf-8")
                if not source.strip():
                    errors.append("empty extracted Markdown")
                errors.extend(asset_errors(file, root))
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
    inventory = {item["id"]: item for item in data["inventory"]}
    objects = data["figures"] + data["tables"]
    registered = {item["id"]: item for item in objects}
    claims = {item["id"]: item for item in data["claims"]}
    for label, sequence in (("inventory", data["inventory"]), ("objects", objects), ("claims", data["claims"])):
        ids = [item["id"] for item in sequence]
        if len(ids) != len(set(ids)):
            errors.append(f"duplicate {label} IDs")
    for key, prefix in (("figures", "Figure "), ("tables", "Table ")):
        if any(not item["id"].startswith(prefix) for item in data[key]):
            errors.append(f"wrong object type in {key}")
    # Caption candidates are only a deterministic backstop to the PDF attestation.
    captions = re.findall(r"^\s*(?:#{1,6}\s+)?(?:\*\*)?((?:Figure|Fig\.?|Table)\s+S?[1-9][0-9]*)\b", prose(source), re.M | re.I)
    for caption in captions:
        identifier = object_refs(caption)[0][0]
        if identifier not in inventory:
            errors.append(f"extracted caption absent from inventory: {identifier}")
    for identifier, item in inventory.items():
        if identifier not in registered:
            errors.append(f"missing interpretation: {identifier}")
    for identifier, item in registered.items():
        inv = inventory.get(identifier)
        if not inv:
            errors.append(f"registered object absent from inventory: {identifier}")
            continue
        if item["scope"] != inv["scope"]:
            errors.append(f"scope mismatch: {identifier}")
        full = item["scope"] == "main" or item["core_argument"] or item["blog_role"] == "used"
        if full:
            for field in ANALYSIS_FIELDS:
                if not item.get(field, "").strip():
                    errors.append(f"{identifier}: missing {field}")
            if not item.get("supported_claim"):
                errors.append(f"{identifier}: missing supported_claim")
            panel_ids = [p["id"] for p in item.get("panels", [])]
            if set(panel_ids) != set(inv["panels"]) or len(panel_ids) != len(set(panel_ids)):
                errors.append(f"{identifier}: panel inventory/analysis mismatch")
        for claim_id in item.get("supported_claim", []):
            if claim_id not in claims:
                errors.append(f"{identifier}: unknown claim {claim_id}")
            elif identifier not in {parent for ref in claims[claim_id]["figure"] for parent, _ in object_refs(ref)}:
                errors.append(f"{identifier}: missing reciprocal evidence link from {claim_id}")
        if len(inv["panels"]) != len(set(inv["panels"])):
            errors.append(f"{identifier}: duplicate inventory panel")
    for identifier, item in claims.items():
        if normalized(item["evidence_text"]) not in normalized(source):
            errors.append(f"{identifier}: evidence excerpt not found in extracted source")
        for ref in item["figure"]:
            target, panel = object_refs(ref)[0]
            if target not in registered or (panel and panel not in inventory.get(target, {}).get("panels", [])):
                errors.append(f"{identifier}: unknown evidence object/panel {ref}")
            elif identifier not in registered[target].get("supported_claim", []):
                errors.append(f"{identifier}: missing reciprocal supported_claim in {target}")
    try:
        text = prose((root / "review/paper-review.md").read_text(encoding="utf-8"))
        blocks = heading_blocks(text, 1)
        for section in SECTIONS:
            found = [body for title, body in blocks if title == section]
            if len(found) != 1 or not found[0].strip():
                errors.append(f"review: missing/duplicate/empty section {section}")
        innovation_section = dict(blocks).get("Claimed innovations", "")
        innovations = [(title, body) for title, body in heading_blocks(innovation_section, 2) if re.fullmatch(r"Innovation [1-9][0-9]*", title)]
        if not innovations:
            errors.append("review: missing innovation assessment (use not established if appropriate)")
        for title, body in innovations:
            for field in INNOVATION_FIELDS:
                match = re.search(r"^- " + re.escape(field) + r":[ \t]*([^\n]*)$", body, re.M)
                if not match or not match[1].strip():
                    errors.append(f"innovation {title}: missing {field}")
                elif field == "Supporting evidence":
                    ids = re.findall(r"\bC[0-9]+\b", match[1])
                    if (not ids and "not established" not in match[1].lower()) or any(i not in claims for i in ids):
                        errors.append(f"innovation {title}: requires known evidence or not established")
        narrative_ids = {i for i, _ in object_refs(dict(blocks).get("Figures and tables", ""))}
        for identifier in registered:
            if identifier not in narrative_ids:
                errors.append(f"review narrative missing {identifier}")
        for identifier, panel in object_refs(text):
            if identifier not in registered or (panel and panel not in inventory.get(identifier, {}).get("panels", [])):
                errors.append(f"review: unknown Figure/Table {identifier}{panel}")
        for claim_id in re.findall(r"\bC[0-9]+\b", text):
            if claim_id not in claims:
                errors.append(f"review: unknown claim {claim_id}")
        if re.search(r"\bTODO\b", text):
            errors.append("unfinished review TODO")
    except OSError as exc:
        errors.append(f"review: {exc}")
    if stage == "review":
        return errors
    if not review["blog_contract_commit"]:
        errors.append("blog contract commit must be recorded after current-rule inspection")
    try:
        file = root / "output/blog.mdx"
        text = file.read_text(encoding="utf-8")
        match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.S)
        if not match:
            return errors + ["blog: missing frontmatter"]
        meta = load_yaml(match[1])
        if not isinstance(meta, dict):
            return errors + ["blog: frontmatter must be a mapping"]
        for field in ("title", "description"):
            if not isinstance(meta.get(field), str) or not meta[field].strip():
                errors.append(f"blog: missing {field}")
        if not isinstance(meta.get("pubDatetime"), (date, datetime)):
            errors.append("blog: pubDatetime must be an unquoted YAML date/timestamp")
        if meta.get("topic") not in {"Wastewater Modelling", "Scientific Machine Learning", "Scientific Computing", "Research Notes"}:
            errors.append("blog: invalid topic")
        if meta.get("draft") is not True:
            errors.append("blog: generated artifact must remain draft=true")
        if "tags" in meta and (not isinstance(meta["tags"], list) or any(not isinstance(tag, str) for tag in meta["tags"])):
            errors.append("blog: tags must be an array of strings")
        for key in ("featured", "hideEditPost"):
            if key in meta and not isinstance(meta[key], bool):
                errors.append(f"blog: {key} must be boolean")
        for key in ("author", "canonicalURL", "timezone", "ogImage"):
            if key in meta and not isinstance(meta[key], str):
                errors.append(f"blog: {key} must be a string")
        if meta.get("modDatetime") is not None and not isinstance(meta["modDatetime"], (date, datetime)):
            errors.append("blog: modDatetime must be a YAML timestamp or null")
        body = prose(text[match.end():])
        blocks = heading_blocks(body, 2)
        for section in BLOG_SECTIONS:
            found = [content for title, content in blocks if title == section]
            if len(found) != 1 or not found[0].strip():
                errors.append(f"blog: missing/duplicate/empty section {section}")
        if re.search(r"^# ", body, re.M) or "TODO" in text:
            errors.append("blog: h1 or unfinished TODO present")
        if not HAN.search(body):
            errors.append("blog: Chinese body required")
        for identifier, panel in object_refs(body):
            if identifier not in registered or (panel and panel not in inventory.get(identifier, {}).get("panels", [])):
                errors.append(f"blog: unknown Figure/Table {identifier}{panel}")
            elif registered[identifier]["blog_role"] != "used":
                errors.append(f"blog: {identifier} not marked used in manifest")
        for identifier, item in registered.items():
            if item["blog_role"] != "used":
                continue
            found = [content for title, content in blocks if title.startswith(identifier + "：") or title.startswith(identifier + ":")]
            if len(found) != 1:
                errors.append(f"blog: requires one evidence section for {identifier}")
                continue
            content = found[0]
            reader_label = "读图方法" if identifier.startswith("Figure") else "读表方法"
            for label in ("问题", reader_label, "核心观察", "支持判断", "证据边界"):
                m = re.search(re.escape(label) + r"：([^\n]+)", content)
                if not m or not HAN.search(m[1]):
                    errors.append(f"blog {identifier}: missing Chinese {label}")
            for claim_id in item.get("supported_claim", []):
                support = re.search(r"支持判断：([^\n]+)", content)
                if not support or claim_id not in re.findall(r"\bC[0-9]+\b", support[1]):
                    errors.append(f"blog {identifier}: support paragraph missing {claim_id}")
            if identifier.startswith("Figure"):
                captions = re.findall(r"<figcaption>(.*?)</figcaption>", content, re.S)
                if not captions or not any(identifier in c and HAN.search(c) for c in captions):
                    errors.append(f"blog {identifier}: missing Chinese figure caption")
                images = re.findall(r"<img\b[^>]*>", content, re.S)
                if not images or any(not re.search(r'\salt\s*=\s*["\'][^"\']*[\u3400-\u9fff][^"\']*["\']', image) for image in images):
                    errors.append(f"blog {identifier}: figure image/Chinese alt required")
                if any(not re.search(r'\ssrc\s*=\s*["\'][^"\']+?["\']', image) for image in images):
                    errors.append(f"blog {identifier}: checked static image src required")
            else:
                before = content.split("<ResponsiveTable", 1)[0]
                if "<ResponsiveTable" not in content or not re.search(r"<p>\s*" + re.escape(identifier) + r"[：:].*?[\u3400-\u9fff].*?</p>", before, re.S):
                    errors.append(f"blog {identifier}: table caption above ResponsiveTable required")
                if not re.search(r"^\s*\|.*\|\s*$|<table\b", content, re.M):
                    errors.append(f"blog {identifier}: missing table content")
        for claim_id in re.findall(r"\bC[0-9]+\b", body):
            if claim_id not in claims:
                errors.append(f"blog: unknown claim {claim_id}")
        errors.extend(asset_errors(file, root))
    except (OSError, ValueError, yaml.YAMLError, RecursionError) as exc:
        errors.append(f"blog: {exc}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--stage", choices=("review", "blog"), default="blog")
    args = parser.parse_args()
    errors = validate(args.workspace, args.stage)
    print("FAIL" if errors else "PASS (deterministic checks only)")
    for error in errors:
        print(f"- {error}")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
