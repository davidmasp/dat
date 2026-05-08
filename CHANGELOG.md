# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-05-08

### Added

- Root `Justfile` recipes for listing templates, copying template folders, and syncing template updates from an upstream `template` remote.
- Documentation for creating new repositories from the template and merging future template updates through a `sync/template-updates` branch.
- Figure panel collection workflow with `figures/input.toml`, checksum-backed `figures/state.toml`, `figures/scripts/figures.py`, and `figures/Justfile` copy/check commands.
- Manuscript starter templates for plain manuscripts and Typst manuscripts, including local artifact copy/check workflows.
- Typst manuscript starter with a `grape-suite` project scaffold, Hayagriva bibliography support, a sample `works.bib`, and a `bib-to-yaml` conversion recipe.
- Data external pipeline template with a `Justfile` and R-based index builder.
- Justfile-based task entry points for `data_pipeline`, `data_simple`, and `sandbox_simple` templates.
- Micromamba Nextflow configuration and VS Code workspace files for analysis and data work.
- Project documentation for analysis, figures, models, reports, and template usage.
- Codex agent instructions for README editing and visualization work.

### Changed

- Reworked template usage around plain directory templates copied by `just create-from-template`.
- Migrated template command wrappers from `Makefile` recipes to `Justfile` recipes.
- Updated the data pipeline template with stricter Nextflow inputs and micromamba-aware configuration.
- Renamed the figure collection configuration from `figures/panels.toml` to `figures/input.toml`.
- Expanded root README guidance with changelog discovery, `uv` install notes, report creation examples, and template-sync instructions.
- Updated data, sandbox, manuscript, and template README files to reflect the current folder-copy workflow.

### Removed

- Legacy `src/datpy` Python package and CLI scaffolding.
- Legacy container and Singularity template scaffolding.
- Top-level `containers/` and `environments/` starter folders.
- Legacy `.datsync.toml` example.
- `config/templates/defaults.toml` and the old `reports_simple` template.
- Template-local `Makefile` wrappers replaced by `Justfile` recipes.

## [0.1.0] - 2024-07-26

### Added

- Initial tagged release of the data analysis project template.
