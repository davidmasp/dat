# Legend metadata and build behavior

## Paths, grouping, and order

`figures.legends.toml` is authored metadata and belongs under Git at the atomic
root. Figure keys are case-sensitive POSIX paths relative to `figures/` with
only the final extension removed. Quote keys containing slashes or dots:
`[plots."qc/coverage.v2"]` matches `figures/qc/coverage.v2.png` and `.pdf`.
Matching stems in different directories remain different plots.

Sections correspond to the first directory under `figures/`. Nested figures
such as `figures/qc/batch-a/coverage.png` appear in section `qc`. Root-level
figures use section `"."`. Section order follows section table declaration
order; plot order within a section follows plot table declaration order.
Unlisted sections/plots follow configured ones in lexical path order. Nested
directories are not separate sections.

Supported formats are PNG, SVG, WebP, JPG, JPEG, GIF, and PDF (case-insensitive).
PNG is the preferred preview, followed by the other image types in that order.
PDF is listed first among downloads. Duplicate extensions for the same stem
(for example `.PNG` and `.png`) fail validation. Hidden paths and HTML reports
are not discovered. The builder requires at least one plot or nonempty text
section; missing configured plots are errors, not silently dropped metadata.

## Schema and example

All fields are optional. Unknown fields or incorrectly typed values fail
validation. `title` and `description` are strings at the root and within section
and plot tables. Descriptions and section `text` are plain text, not HTML or
Markdown; blank lines separate paragraphs. A legend can therefore use `<`, `>`,
and other scientific notation literally. TOML comments are for maintainers.

```toml
title = "Study figure library"
description = "Existing outputs from the current analysis."

[sections."qc"]
title = "Quality control"
description = "Coverage and library metrics after the documented sample filters."

[sections."notes"]
title = "Methods note"
description = "Context for interpreting these figures."
text = """
Summarize the method and its limits using the actual analysis as evidence.

Explain relevant caveats or link to a longer local note below.
"""
source = "docs/methods.md"
link_label = "Read the methods note"
download = false

[plots."qc/coverage"]
title = "Coverage by sample"
description = """
State the plotted variables and units, what the colors represent, and any
important filtering. Record a supported interpretation and the producing script.
"""

[plots."qc/report"]
title = "Full QC report"
description = "The saved multipage report."
download_only = true
```

The example keys must be adapted to real files before use. There is no separate
numeric order field; declaration order is the source of truth. Avoid dotted,
unquoted plot keys, which TOML interprets as nested tables.

`download_only = true` requires a PDF at the exact plot key. It suppresses
that plot's image preview and image-only siblings matching `<key>_<digits>`,
which is useful for page exports. Siblings with their own PDFs remain distinct
entries. Do not set it when those numbered images are independent plots.
Without this flag, a PDF-only file also appears as a download entry naturally.

Text-only sections require nonempty `text` and no figure folder with the same
section key. Optional `source` identifies a local file relative to the TOML's
directory; it must exist within the atomic root. `link_label` customizes its
link, and `download = true` adds the download attribute. Both require `source`;
`source` requires `text`. Text-section IDs must not collide with plot IDs.

## Commands and outputs

From the atomic root:

```bash
uv run scripts/build_figure_gallery.py
uv run scripts/build_figure_gallery.py --output figures/gallery.html
```

All explicit relative paths are relative to `--root` (default: current working
directory), including `--template`. Defaults are `--figure-dir figures`,
`--legends figures.legends.toml`, and `--output <figure-dir>/index.html`.
The template defaults to `figure_gallery.html` beside the copied builder, or
the skill's bundled `assets/figure_gallery.html` when run directly from the
skill. An alternate template must retain `@@GALLERY_TITLE@@`,
`@@GALLERY_DESCRIPTION@@`, and `@@GALLERY_DATA@@` plus the corresponding data
schema and browser behavior. Prefer the bundled template for a consistent UI.

To build directly without setup, for example during inspection:

```bash
uv run /path/to/figure-gallery/scripts/build_figure_gallery.py --root /path/to/atomic-folder
```

The archive is always `figure_gallery.zip` next to the selected HTML output.
It contains that HTML and only the image/PDF downloads and configured source
files linked by the gallery, with paths relative to the atomic root. It excludes
unlinked outputs, page previews suppressed by `download_only`, TOML metadata,
builders, and section-level HTML reports. Source documents are copied as
individual files: transitive resources linked inside a Markdown/HTML document
are not recursively bundled. Keep source notes self-contained or share their
extra resources separately. A source link to an analysis script includes that
script; check the requested sharing scope before choosing source files.

Paths outside the atomic root, including escaping symlinks, are rejected.
Links retain URL escaping for spaces, Unicode, `#`, and `%`. Existing figures
are never modified. Both HTML and ZIP are staged after metadata and bundle
validation; a validation failure preserves the previous build. Generated HTML
contains a marker used to distinguish it from unrelated reports. The explicit
`--replace-existing-gallery` option permits migration of an inspected existing
index; ordinary rebuilds do not need it.

## Reference provenance

The bundled template and builder were adapted from the user's existing
`data/lpwgs_rome` gallery in the `gsce` project. The reusable version preserves
that offline library UI while using an explicit atomic root, checking stale
plot metadata and bundle paths, and staging both outputs before publication.
No source project, external assets, or scientific example data are needed at
runtime. Project-specific sections and legend text are intentionally absent.
