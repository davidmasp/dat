---
name: figure-gallery
description: Create or maintain an offline HTML figure gallery in a DAT atomic analysis or data folder, with Git-tracked TOML legends and a portable ZIP. Use when a gallery is requested or an existing gallery needs updating as figures are produced.
---

# Figure Gallery

Build a browsable library of existing figures within one atomic folder. Keep
figures in `figures/<topic>/`; combine matching relative paths and stems into
one plot entry. Gallery builds do not run analyses, render PDFs into images,
or move source figures. Use the bundled HTML template to preserve the reference
interface: collapsible section/plot navigation, search, hash permalinks,
previous/next plot controls, zoom, and original downloads.

## Set up or maintain a gallery

Inspect the target folder's README, Justfile, figure paths, and any existing
gallery implementation. Use the atomic folder's established layout and working
directory. This skill complements `dat-atomic-folder`; creating an entire new
atomic folder is a separate step governed by that workflow when requested.

For first-time setup, run this skill's helper with the existing atomic folder:

```bash
uv run /path/to/figure-gallery/scripts/setup_gallery.py /path/to/atomic-folder
```

The helper copies the builder and template into `scripts/`, creates a starter
`figures.legends.toml` only when absent, and ensures `figures/` exists. It refuses
conflicting builder/template files before copying anything. Inspect and merge
an existing implementation deliberately; do not replace local customizations
with the bundled version as a side effect of rebuilding.

Track these reusable inputs:

- `scripts/build_figure_gallery.py`
- `scripts/figure_gallery.html`
- `figures.legends.toml` at the atomic root, outside ignored outputs

Merge `/figures/` into the local `.gitignore` if absent. Preserve existing ignore
rules and ensure legends and scripts are trackable. Generated images, PDFs,
HTML, and ZIPs remain local outputs. Add this recipe to the existing root
Justfile, keeping its dotenv conventions and other recipes:

```just
# Build an offline gallery from existing figures and TOML legends.
build-figure-gallery:
    uv run scripts/build_figure_gallery.py
```

## Write legends as figures are produced

Read [references/legends.md](references/legends.md) when creating or editing
metadata. Preserve authored titles, descriptions, and ordering unless the task
requires a change. For each produced or changed plot, update its TOML entry
using the generating script, actual figure, and available results as evidence.
Describe the variables, axes and units, groups and encodings, material filters
or transformations, and a brief interpretation with relevant limits. Keep it
brief; mention the producing script when useful for provenance. Use section
descriptions for shared methods rather than repeating them for every plot.

Do not infer scientific conclusions from filenames or invent missing methods.
Inspect source code or outputs to resolve uncertainty, and state material
unknowns plainly. Auto-discovered entries may have filename-derived titles and
empty descriptions; fill their legends when evidence is available. Do not
delete authored metadata simply to make a missing-output check pass.

For new plot generation under DAT conventions, export PDF and PNG companions
with matching stems and physical dimensions. Existing PDF-only reports still
work as downloads; rebuilding a gallery does not authorize rerunning their
analysis. Download-only reports and text sections are optional metadata choices,
not defaults for a particular scientific topic.

## Build, verify, and document

Run from the atomic root:

```bash
uv run scripts/build_figure_gallery.py
# Or: just build-figure-gallery
```

The Python 3.11+ helper uses only the standard library and inline uv metadata;
no new project environment or dependencies are needed. It writes
`figures/index.html` and `figures/figure_gallery.zip`. It discovers unlisted
figures, validates configured plots and source links, and packages only linked
files with atomic-root-relative paths. Per-topic HTML reports are left alone.
If the root index is an existing report, inspect downstream consumers and use
another `--output` path, or deliberately migrate it using
`--replace-existing-gallery` after checking it can be replaced.

Open the generated HTML and check navigation/collapse, search (including no
matches), a bookmarked plot hash, previous/next, image loading, zoom, downloads,
and narrow layout. Check PDF-only and text entries when present. Extract the ZIP
to another directory and confirm linked files still resolve. The gallery works
via `file://` without a server or network; preserve the extracted directory tree.
See [references/legends.md](references/legends.md) for CLI options and bundle
boundaries. If browser verification is unavailable, report that limitation.

Update the atomic README with the builder and template roles, legend-editing
workflow, command, outputs, checks actually performed, and sharing guidance.
Return the gallery path and reproduction command. For skill maintenance, run:

```bash
uv run /path/to/figure-gallery/scripts/test_figure_gallery.py
```
