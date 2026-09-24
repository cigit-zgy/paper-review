"""Offline contract tests. No network, real papers, MinerU models or pytest."""
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_review import validate  # noqa: E402
from extract_pdf import import_extracted, build_command, unpack_bundle  # noqa: E402


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="paper review tests ")
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name) / "review workspace"
        shutil.copytree(ROOT / "tests/fixtures/minimal", self.work)
        (self.work / "source").mkdir()
        # A source-presence stub, never sent to MinerU or represented as a real PDF.
        (self.work / "source/paper.pdf").write_bytes(b"%PDF-1.4\n% synthetic test stub\n")
        self.manifest = self.work / "review/manifest.yaml"

    def edit(self, change):
        data = yaml.safe_load(self.manifest.read_text())
        change(data)
        self.manifest.write_text(yaml.safe_dump(data, sort_keys=False))

    def rejects(self, needle=None, stage="blog"):
        errors = validate(self.work, stage)
        self.assertTrue(errors, "incomplete artifact unexpectedly passed")
        if needle:
            self.assertIn(needle, "\n".join(errors))

    def test_valid_minimal_review_and_blog(self):
        self.assertEqual(validate(self.work, "review"), [])
        self.assertEqual(validate(self.work, "blog"), [])

    def test_missing_figure_analysis(self):
        self.edit(lambda m: m["figures"].clear())
        self.rejects("Figure 1")

    def test_missing_table_analysis(self):
        self.edit(lambda m: m["tables"].clear())
        self.rejects("Table 1")

    def test_missing_interpretation(self):
        self.edit(lambda m: m["figures"][0].pop("authors_interpretation"))
        self.rejects("authors_interpretation")

    def test_innovation_evidence_or_uncertainty(self):
        path = self.work / "review/paper-review.md"
        original = path.read_text()
        path.write_text(original.replace("Supporting evidence: C01", "Supporting evidence: unsupported assertion"))
        self.rejects("innovation")
        path.write_text(original.replace("Supporting evidence: C01", "Supporting evidence: not established — synthetic illustration only"))
        self.assertEqual(validate(self.work, "blog"), [])

    def test_blog_nonexistent_figure(self):
        path = self.work / "output/blog.mdx"
        path.write_text(path.read_text() + "\nFigure 9：不存在。\n")
        self.rejects("Figure 9")

    def test_missing_chinese_section(self):
        path = self.work / "output/blog.mdx"
        path.write_text(path.read_text().replace("## 创新点在哪里？", "## 其他"))
        self.rejects("创新点在哪里")

    def test_malformed_manifest(self):
        self.manifest.write_text("paper: [broken")
        self.rejects("manifest")

    def test_wrong_manifest_type(self):
        self.manifest.write_text("[]")
        self.rejects("manifest")

    def test_duplicate_yaml_key(self):
        self.manifest.write_text(self.manifest.read_text() + "\npaper: {}\n")
        self.rejects("duplicate")

    def test_spaces_and_cli(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate_review.py"), str(self.work)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_asset(self):
        (self.work / "extracted/assets/figure-1.svg").unlink()
        self.rejects("asset")

    def test_missing_panel(self):
        self.edit(lambda m: m["figures"][0]["panels"].pop())
        self.rejects("panel")

    def test_invented_claim(self):
        self.edit(lambda m: m["figures"][0]["supported_claim"].append("C99"))
        self.rejects("C99")

    def test_invented_evidence_quote(self):
        self.edit(lambda m: m["claims"][0].update(evidence_text="This was never in the source."))
        self.rejects("excerpt")

    def test_blocking_uncertainty(self):
        self.edit(lambda m: m["review"]["uncertainties"].append({"source_location": "p. 2", "issue": "Unreadable axes", "blocks_blog": True}))
        self.rejects("uncertainty", "review")

    def test_inventory_not_checked(self):
        self.edit(lambda m: m["review"].update(inventory_checked=False))
        self.rejects("inventory_checked", "review")

    def test_inventory_cannot_hide_extracted_caption(self):
        self.edit(lambda m: (m["inventory"].clear(), m["figures"].clear(), m["tables"].clear()))
        self.rejects("caption", "review")

    def test_asset_escape(self):
        path = self.work / "output/blog.mdx"
        path.write_text(path.read_text() + '\n<img src="../../../outside.svg" alt="路径越界" />\n')
        self.rejects("outside")

    def test_caption_and_evidence_boundary_required(self):
        path = self.work / "output/blog.mdx"
        original = path.read_text()
        path.write_text(original.replace("证据边界：", "补充："))
        self.rejects("证据边界")
        path.write_text(original.replace("<figcaption>", "<p>").replace("</figcaption>", "</p>"))
        self.rejects("caption")

    def test_invalid_frontmatter(self):
        path = self.work / "output/blog.mdx"
        path.write_text(path.read_text().replace('topic: "Research Notes"', 'topic: "Unknown"'))
        self.rejects("topic")

    def test_invalid_tags(self):
        path = self.work / "output/blog.mdx"
        path.write_text(path.read_text().replace("tags: []", "tags: wrong-type"))
        self.rejects("tags")

    def test_missing_asset_with_spaced_attribute(self):
        path = self.work / "output/blog.mdx"
        path.write_text(path.read_text().replace('src="../extracted/assets/figure-1.svg"', 'src = "../extracted/assets/nonexistent.svg"'))
        self.rejects("asset")

    def test_image_missing_src(self):
        path = self.work / "output/blog.mdx"
        path.write_text(path.read_text().replace('src="../extracted/assets/figure-1.svg"', ''))
        self.rejects("src")

    def test_claim_object_bidirectional_consistency(self):
        self.edit(lambda m: m["claims"][0].update(figure=["Table 1"]))
        self.rejects("reciprocal")

    def test_empty_innovation_field(self):
        path = self.work / "review/paper-review.md"
        original = path.read_text()
        from validate_review import INNOVATION_FIELDS
        import re
        for field in INNOVATION_FIELDS:
            with self.subTest(field=field):
                path.write_text(re.sub(r'^- '+re.escape(field)+r':[^\n]*', '- '+field+':', original, flags=re.M))
                self.rejects(field)

    def test_unknown_review_references(self):
        path = self.work / "review/paper-review.md"
        path.write_text(path.read_text() + '\nC99 is supported by Figure 99.\n')
        self.rejects("unknown claim C99", "review")

    def test_valid_spaced_image_attributes(self):
        path = self.work / "output/blog.mdx"
        path.write_text(path.read_text().replace('src=', 'src = ').replace('alt=', 'alt = '))
        self.assertEqual(validate(self.work, "blog"), [])

    def test_missing_reciprocal_object_claim(self):
        self.edit(lambda m: m["claims"].append({**m["claims"][0], "id": "C02"}))
        self.rejects("reciprocal")

    def test_init_no_overwrite_and_no_premature_blog(self):
        destination = Path(self.temp.name) / "new workspace"
        command = [sys.executable, str(ROOT / "scripts/init_review.py"), str(self.work / "source/paper.pdf"), str(destination)]
        first = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertFalse((destination / "output/blog.mdx").exists())
        second = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(second.returncode, 0)
        self.assertTrue(validate(destination, "review"))

    def test_import_bundle_and_no_overwrite(self):
        dest = Path(self.temp.name) / "import workspace"
        dest.mkdir()
        import_extracted(self.work / "extracted/paper.md", dest / "extracted")
        self.assertTrue((dest / "extracted/assets/figure-1.svg").is_file())
        with self.assertRaises((ValueError, FileExistsError)):
            import_extracted(self.work / "extracted/paper.md", dest / "extracted")

    def test_local_full_document_command(self):
        command = build_command(Path("/existing env/bin/mineru-kit"), self.work / "source/paper.pdf", self.work / "bundle.zip", "standard")
        self.assertEqual(command[0], "/existing env/bin/mineru-kit")
        self.assertIn("all", command)
        self.assertIn("zip", command)
        self.assertNotIn("--remote", command)

    def test_fake_mineru_end_to_end(self):
        """Real subprocess adapter, fake executable, no parser/model/network."""
        base = Path(self.temp.name)
        bindir = base / "fake mineru bin"
        bindir.mkdir()
        cli = bindir / "mineru"
        cli.write_text(f'#!{sys.executable}\nprint("MinerU version: 4.0.2")\n')
        kit = bindir / "mineru-kit"
        kit.write_text(f'''#!{sys.executable}
import sys, zipfile
from pathlib import Path
if "--help" in sys.argv:
    print("--output --format --pages --tier zip")
else:
    assert "--remote" not in sys.argv
    assert sys.argv[sys.argv.index("--pages") + 1] == "all"
    fixture = Path({str(ROOT / 'tests/fixtures/minimal/extracted')!r})
    with zipfile.ZipFile(sys.argv[sys.argv.index("--output") + 1], "w") as z:
        for p in fixture.rglob("*"):
            if p.is_file(): z.write(p, p.relative_to(fixture))
''')
        cli.chmod(0o755)
        kit.chmod(0o755)
        destination = base / "new full flow"
        init = subprocess.run([sys.executable, str(ROOT / "scripts/init_review.py"), str(self.work / "source/paper.pdf"), str(destination)], capture_output=True, text=True)
        self.assertEqual(init.returncode, 0, init.stderr)
        extraction = subprocess.run([sys.executable, str(ROOT / "scripts/extract_pdf.py"), str(destination), "--mineru-kit", str(kit)], capture_output=True, text=True)
        self.assertEqual(extraction.returncode, 0, extraction.stderr)
        shutil.copytree(self.work / "review", destination / "review", dirs_exist_ok=True)
        self.assertEqual(validate(destination, "review"), [])
        self.assertFalse((destination / "output/blog.mdx").exists())
        shutil.copy2(self.work / "output/blog.mdx", destination / "output/blog.mdx")
        self.assertEqual(validate(destination, "blog"), [])

    def test_zip_path_escape_rejected(self):
        archive = Path(self.temp.name) / "invalid.zip"
        with zipfile.ZipFile(archive, "w") as bundle:
            bundle.writestr("../outside.md", "unsafe")
        with self.assertRaisesRegex(ValueError, "unsafe"):
            unpack_bundle(archive, Path(self.temp.name) / "unpacked")

    def test_extracted_symlink_rejected(self):
        link = self.work / "extracted/assets/external.svg"
        link.symlink_to(self.work / "extracted/assets/figure-1.svg")
        with self.assertRaisesRegex(ValueError, "symlink"):
            import_extracted(self.work / "extracted/paper.md", Path(self.temp.name) / "other")


if __name__ == "__main__":
    unittest.main(verbosity=2)
