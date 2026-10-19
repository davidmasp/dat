#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Exercise setup/build/bundling; optionally create a synthetic browser fixture."""

import argparse
import base64
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote
import zipfile

import build_figure_gallery as gallery
from setup_gallery import setup


PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aX1sAAAAASUVORK5CYII="
)
PDF = b"%PDF-1.4\n% Synthetic download fixture; not an analysis output.\n%%EOF\n"
SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="480" viewBox="0 0 900 480">
<rect width="900" height="480" fill="white"/>
<text x="55" y="65" font-family="sans-serif" font-size="28" fill="#1f2e35">Synthetic preview fixture</text>
<text x="55" y="100" font-family="sans-serif" font-size="16" fill="#637079">For gallery interaction checks; no research data.</text>
<rect x="55" y="145" width="225" height="240" rx="8" fill="#eaf4f1"/>
<rect x="330" y="145" width="225" height="240" rx="8" fill="#f5f8f8"/>
<rect x="605" y="145" width="225" height="240" rx="8" fill="#eaf4f1"/>
<g font-family="sans-serif" font-size="24" fill="#176b65"><text x="130" y="280">A</text>
<text x="410" y="280">B</text><text x="685" y="280">C</text></g></svg>'''
LEGENDS = '''title = "Synthetic gallery"
description = "Builder and browser checks using synthetic files."
[sections."qc"]
title = "Quality control"
description = "Shared section context: synthetic fixtures only."
[sections."methods"]
title = "Methods note"
text = "A text-only entry with a local source link."
source = "docs/source #1.md"
link_label = "Read fixture source"
[plots."qc/second"]
title = "Second preview"
description = "Tests configured ordering before the first filename."
[plots."qc/first"]
title = "First preview"
description = "Synthetic diagram; tests zoom and original downloads."
[plots."qc/report"]
title = "Download-only report"
download_only = true
'''


def fixture(root: Path) -> None:
    setup(root)
    files = {
        "figures/qc/first.svg": SVG.encode(),
        "figures/qc/first.pdf": PDF,
        "figures/qc/second.svg": SVG.encode(),
        "figures/qc/report.pdf": PDF,
        "figures/qc/report_1.png": PNG,
        "figures/extras/plot #é%.png": PNG,
        "figures/root.png": PNG,
        "figures/qc/index.html": b"Existing per-topic report",
        "figures/.hidden/skip.png": PNG,
        "docs/source #1.md": b"Self-contained synthetic fixture note.\n",
    }
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    (root / "figures.legends.toml").write_text(LEGENDS, encoding="utf-8")


def payload(document: str) -> dict:
    return json.loads(re.search(
        r'<script id="gallery-data" type="application/json">(.*?)</script>', document, re.S,
    )[1])


def build(root: Path, legends: Path | None = None) -> tuple[str, list[dict]]:
    return gallery.build_gallery(
        root / "figures", legends or root / "figures.legends.toml", root / "figures/index.html",
    )


class GalleryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="figure-gallery-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        fixture(self.root)

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(self.root / "scripts/build_figure_gallery.py"), *args],
            cwd=self.root, capture_output=True, text=True,
        )

    def test_setup_is_repeatable_and_preserves_authored_legends(self):
        before = (self.root / "figures.legends.toml").read_bytes()
        self.assertEqual(setup(self.root), [])
        self.assertEqual((self.root / "figures.legends.toml").read_bytes(), before)

    def test_setup_preflights_conflicts_without_partial_copies(self):
        target = self.root / "existing"
        (target / "scripts").mkdir(parents=True)
        (target / "scripts/figure_gallery.html").write_text("custom")
        with self.assertRaisesRegex(ValueError, "differs"):
            setup(target)
        self.assertFalse((target / "scripts/build_figure_gallery.py").exists())
        self.assertFalse((target / "figures.legends.toml").exists())

    def test_grouping_order_download_only_and_unlisted_entries(self):
        _, sections = build(self.root)
        self.assertEqual([s["id"] for s in sections], ["qc", "methods", ".", "extras"])
        plots = sections[0]["plots"]
        self.assertEqual([p["id"] for p in plots], ["qc/second", "qc/first", "qc/report"])
        self.assertEqual([f["format"] for f in plots[1]["files"]], ["PDF", "SVG"])
        self.assertIsNone(plots[2]["preview"])
        self.assertEqual([f["format"] for f in plots[2]["files"]], ["PDF"])
        self.assertIn("%23%C3%A9%25", sections[3]["plots"][0]["preview"])
        self.assertEqual(sections[1]["source"], "../docs/source%20%231.md")

    def test_png_preference_nested_paths_and_independent_stems(self):
        (self.root / "figures/qc/first.png").write_bytes(PNG)
        nested = self.root / "figures/qc/nested/first.png"
        nested.parent.mkdir()
        nested.write_bytes(PNG)
        _, sections = build(self.root)
        plots = {p["id"]: p for p in sections[0]["plots"]}
        self.assertEqual(plots["qc/first"]["preview"], "qc/first.png")
        self.assertIn("qc/nested/first", plots)
        self.assertEqual(len(plots["qc/first"]["files"]), 3)

    def test_plain_pdf_without_flag(self):
        (self.root / "figures/extras/plain.pdf").write_bytes(PDF)
        _, sections = build(self.root)
        plot = next(p for s in sections for p in s["plots"] if p["id"] == "extras/plain")
        self.assertIsNone(plot["preview"])
        self.assertEqual(plot["files"][0]["format"], "PDF")

    def test_legend_json_cannot_close_script(self):
        value = '</script><script>window.pwned=true</script> @@GALLERY_TITLE@@'
        path = self.root / "figures.legends.toml"
        path.write_text('title = "<Research & figures>"\n[plots."qc/first"]\ndescription = '
                        + json.dumps(value), encoding="utf-8")
        document, _ = build(self.root)
        self.assertIn("&lt;Research &amp; figures&gt;", document)
        self.assertNotIn("<script>window.pwned", document)
        entry = next(p for s in payload(document)["sections"] for p in s["plots"]
                     if p["id"] == "qc/first")
        self.assertEqual(entry["description"], value)

    def test_validation_rejects_bad_metadata(self):
        cases = [
            ('unexpected = true', "Unknown legend"),
            ('[plots."qc/missing"]\ntitle = "Absent"', "not found"),
            ('[plots."qc/first"]\ndownload_only = true', "requires a PDF"),
            ('[plots."qc/first"]\ndownload_only = "true"', "true or false"),
            ('[sections."qc"]\ntext = "Conflicting text"', "cannot also contain figures"),
            ('[sections."note"]\nsource = "docs/source #1.md"', "requires a text"),
            ('[sections."note"]\ntext = "Note"\ndownload = true', "requires a source"),
            ('[plots."../outside"]\ntitle = "Invalid"', "Invalid plots key"),
            ('[sections."nested/path"]\ntitle = "Invalid"', "top-level"),
            ('[plots.qc.first]\ntitle = "Incorrect TOML nesting"', "Invalid settings"),
        ]
        (self.root / "figures/qc/first.pdf").unlink()
        for content, message in cases:
            with self.subTest(content=content):
                (self.root / "figures.legends.toml").write_text(content)
                with self.assertRaisesRegex(ValueError, message):
                    build(self.root)

    def test_text_only_and_empty_gallery(self):
        root = self.root / "text-only"
        root.mkdir()
        setup(root)
        with self.assertRaisesRegex(ValueError, "No supported"):
            build(root)
        (root / "figures.legends.toml").write_text('[sections.note]\ntext = "Only text"')
        document, sections = build(root)
        self.assertEqual(sections[0]["plots"], [])
        self.assertEqual(payload(document)["sections"][0]["text"], "Only text")

    def test_cli_bundle_is_portable_and_contains_only_linked_files(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        output = self.root / "figures/index.html"
        with zipfile.ZipFile(self.root / "figures/figure_gallery.zip") as archive:
            names = archive.namelist()
            self.assertIn("figures/index.html", names)
            self.assertIn("docs/source #1.md", names)
            self.assertNotIn("figures/qc/report_1.png", names)
            self.assertNotIn("figures/qc/index.html", names)
            self.assertNotIn("figures.legends.toml", names)
            extracted = self.root / "moved"
            archive.extractall(extracted)
        moved_output = extracted / "figures/index.html"
        self.assertEqual(output.read_bytes(), moved_output.read_bytes())
        for section in payload(moved_output.read_text())["sections"]:
            links = [f["url"] for p in section["plots"] for f in p["files"]]
            if section.get("source"):
                links.append(section["source"])
            for url in links:
                self.assertTrue((moved_output.parent / unquote(url)).is_file(), url)
        self.assertEqual(self.run_cli().returncode, 0)  # A generated index can be rebuilt.

    def test_failed_bundle_preserves_previous_outputs(self):
        self.assertEqual(self.run_cli().returncode, 0)
        output = self.root / "figures/index.html"
        archive = self.root / "figures/figure_gallery.zip"
        before = (output.read_bytes(), archive.read_bytes())
        path = self.root / "figures.legends.toml"
        path.write_text(LEGENDS.replace('docs/source #1.md', '../outside.md'))
        outside = self.root.parent / (self.root.name + "-outside.md")
        outside.write_text("Outside root")
        self.addCleanup(outside.unlink)
        path.write_text(LEGENDS.replace('docs/source #1.md', '../' + outside.name))
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("inside the atomic folder", result.stderr)
        self.assertEqual((output.read_bytes(), archive.read_bytes()), before)

    def test_existing_report_guard_and_output_override(self):
        output = self.root / "figures/index.html"
        output.write_text("Existing report")
        self.assertNotEqual(self.run_cli().returncode, 0)
        self.assertEqual(output.read_text(), "Existing report")
        self.assertEqual(self.run_cli("--output", "figures/gallery.html").returncode, 0)
        self.assertEqual(output.read_text(), "Existing report")
        self.assertEqual(self.run_cli("--replace-existing-gallery").returncode, 0)
        self.assertIn(gallery.GENERATED_MARKER, output.read_text())

    def test_outside_output_and_escaping_symlink_are_rejected(self):
        result = self.run_cli("--output", "../outside.html")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("inside the atomic folder", result.stderr)
        link = self.root / "figures/qc/escape.svg"
        link.symlink_to(Path(__file__).resolve())
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("inside the atomic folder", result.stderr)

    def test_direct_skill_builder_resolves_explicit_atomic_root(self):
        result = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("build_figure_gallery.py")),
             "--root", str(self.root)], capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo-root", type=Path, help="Create synthetic gallery in a NEW directory")
    args, remaining = parser.parse_known_args()
    if args.demo_root:
        root = args.demo_root.resolve()
        root.mkdir(parents=True, exist_ok=False)
        fixture(root)
        document, sections = build(root)
        gallery.write_outputs(document, root / "figures/index.html", sections, root)
        with zipfile.ZipFile(root / "figures/figure_gallery.zip") as archive:
            archive.extractall(root / "extracted")
        print(root / "figures/index.html")
    else:
        unittest.main(argv=[sys.argv[0], *remaining])


if __name__ == "__main__":
    main()
