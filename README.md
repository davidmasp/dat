# DAT

See [.dat.docs.md](.dat.docs.md) for more information about the repository and
its structure.

## Figure galleries

Use the local [`figure-gallery` skill](.agents/skills/figure-gallery/SKILL.md)
alongside `dat-atomic-folder` to build an offline library from existing figures.
It provides a setup helper, reusable Python builder, shared HTML template, and
TOML legend guidance. From the repository root, initialize an existing atomic
folder with:

```bash
uv run .agents/skills/figure-gallery/scripts/setup_gallery.py analysis/my-analysis
```

Edit that folder's `figures.legends.toml`, then run
`uv run scripts/build_figure_gallery.py` from its root. The builder groups
matching image/PDF stems and writes `figures/index.html` plus
`figures/figure_gallery.zip`, preserving relative links for offline sharing.
Keep the TOML and gallery code under Git; generated outputs stay ignored.
The skill covers merging the Justfile recipe and documenting the gallery in
the atomic README.

Reproduce the helper checks from this repository root:

```bash
uv run .agents/skills/figure-gallery/scripts/test_figure_gallery.py
```

Validation covered 13 tests, an independent fresh-folder workflow, and browser
checks for collapse, search, hash links, paging, image loading, zoom, download
and source URLs, PDF-only/text entries, and a 390px layout. All linked files
resolved after ZIP extraction. Browser checks used a temporary localhost
server because the preview tool rejects `file://`; direct local-file browsing
was not exercised by automation. Tests use temporary synthetic fixtures, not
research outputs. Generate a fixture for manual browser checks with
`uv run .agents/skills/figure-gallery/scripts/test_figure_gallery.py --demo-root /tmp/gallery-demo`
(the destination must not already exist).

---

AFTER CREATION OF THIS REPOSITORY, INCLUDE DOCUMENTATION HERE.
