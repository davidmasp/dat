---
name: dat-templates
description:
  Help Codex use the DAT repository template system. Use when working in this
  repo and asked to choose a starter folder under `config/templates`, create a
  new `data`, `sandbox`, `analysis`, `metadata`, `models`, or `writting` project
  area from a template, explain `just list-templates` or `just
  create-from-template`, or adapt a copied template to DAT conventions.
metadata:
  short-description: Use DAT repo folder templates
---

# DAT Templates

Use the repository's built-in folder templates instead of hand-rolling new
project areas.

## Workflow

1. Confirm the requested work belongs in this repository and should start from
   `config/templates`.
2. Run `just list-templates` if the best template is not already obvious.
3. Map the request to a destination path rooted at the repo, such as `data/...`,
   `sandbox/...`, or `writting/...`.
4. Copy the starter with
   `just create-from-template <template-name> <destination-path>`.
5. Replace placeholders, local paths, and sample artifact references in the
   copied folder.
6. Read the copied template's local `README.md` or `Justfile` before making
   follow-up edits.

## Selection Rules

- Prefer the smallest template that fits; do not start from a pipeline template
  when a simple shell or R starter is enough.
- Use `data_simple` for lightweight fetch-or-clean folders.
- Use `data_pipeline` for in-repo Nextflow pipelines that produce data, tables,
  or figures.
- Use `data_external_pipeline` when the repo only wraps an external Nextflow
  pipeline and needs an index builder plus execution stub.
- Use `sandbox_simple` for exploratory analysis or scratch work.
- Use `manuscript_simple` or `manuscript_typst` for writing artifacts that need
  local copied figures and tables.

## Path Rules

- Treat the destination as repo-relative; `just create-from-template` does a
  direct `cp -R`.
- Follow the DAT folder taxonomy from `.dat.docs.md` for code-producing areas:
  `data`, `analysis`, `metadata`, `models`, and `sandbox`.
- Place manuscripts, slides, and reports under `writting/` in this repo, even
  though some examples in the docs still say `manuscripts/`.
- Refuse to overwrite an existing destination; choose a new folder name or let
  the user decide.

## After Copying

- Update placeholder titles, dates, author names, pipeline paths, scratch paths,
  and sample artifact references immediately.
- Check the copied `Justfile` for the expected entrypoints such as `just all`,
  `just download`, `just pipeline`, `just artifacts`, or `just compile`.
- For manuscript templates, review `artifacts/input.toml` and remove example
  figure and table paths before the folder is treated as real.
- For pipeline templates, inspect `nextflow.config`, profile defaults, and clean
  scripts before running anything destructive.

## References

- Read `references/template-catalog.md` when you need the concrete template
  list, command behavior, or repo-specific path guidance.
