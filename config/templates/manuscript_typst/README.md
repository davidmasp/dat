# Manuscript Folder

Minimal starter folder for a Typst manuscript.

Keep manuscript text and local pulled assets together here. The `artifacts/`
subfolder is the manuscript-local equivalent of the current global `figures/`
workflow: configure source files in `artifacts/input.toml`, pull them locally,
and verify them with checksums.

Compile the manuscript with:

```bash
just compile
```

Convert the sample BibTeX bibliography to Hayagriva YAML for Typst with:

```bash
just bib-to-yaml
```

You can also pass explicit paths:

```bash
just bib-to-yaml references.bib references.yaml
```
