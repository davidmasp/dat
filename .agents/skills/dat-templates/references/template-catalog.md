# DAT Template Catalog

Use this reference when you need the concrete starter list or need to explain
how the repo's template copy flow works.

## Root Commands

`Justfile` defines the template entrypoints:

- `just list-templates`: list the directories directly under `config/templates`.
- `just create-from-template <template-name> <destination-path>`: copy one
  template folder to a repo-relative destination.
- `just template-add-remote`: add the upstream DAT template remote to a
  generated repository.
- `just template-sync`: fetch `template/main`, create `sync/template-updates`,
  and merge upstream template changes for review.

`create-from-template` fails if:

- the template directory does not exist
- the destination path already exists

The implementation is a plain recursive copy, so all placeholders and sample
files come across unchanged.

## Repo Placement Conventions

`.dat.docs.md` defines the main project areas:

- `src`: project-specific packages and libraries
- `data`: atomic folders that produce data
- `analysis`: atomic folders that produce figures and tables
- `metadata`: sample and study metadata
- `sandbox`: exploratory or throwaway work
- `models`: predictive model training folders
- `writting`: manuscripts, slides, reports, and other no-code writing artifacts

Use these as default destinations when the user asks where a copied template
should live.

## Available Templates

### `data_simple`

Use for lightweight data acquisition or preparation.

- Files: `Justfile`, `README.md`, `make.sbatch`, `scripts/download.sh`,
  `scripts/clean.sh`
- Entry points: `just download`, `just all`, `just clean`
- Typical destination: `data/<name>`

### `data_pipeline`

Use for in-repo Nextflow data pipelines.

- Files: `main.nf`, `nextflow.config`, `Justfile`, `bin/bin.sh`, scripts for
  download, index building, and cleanup
- Entry points: `just download`, `just index`, `just pipeline`, `just all`,
  `just clean`
- Notes: profile defaults include `micromamba,slurm,tower`; clean script removes
  `data`, `raw`, and marker files
- Typical destination: `data/<pipeline-name>`

### `data_external_pipeline`

Use when the actual Nextflow pipeline lives elsewhere and this repo only
prepares inputs and runs it.

- Files: `Justfile`, `scripts/build_index.R`
- Entry points: `just index`, `just run`, `just clean-scratch`
- Notes: replace `/path/to/pipeline`, `/path/to/scratch`, and profile defaults
  before use
- Typical destination: `data/<external-run-name>`

### `sandbox_simple`

Use for exploratory analysis or quick figure generation.

- Files: `Justfile`, `README.md`, `scripts/plot.R`, `scripts/clean.sh`
- Entry points: `just plot`, `just all`, `just clean`
- Typical destination: `sandbox/<name>`

### `manuscript_simple`

Use for manuscripts that do not need Typst.

- Files: `Justfile`, `README.md`, `artifacts/` subfolder with its own
  `Justfile`, `input.toml`, `state.toml`, and `scripts/artifacts.py` runner
- Entry points: `just artifacts`, `just check-artifacts`
- Notes: copied artifact paths are local to the manuscript folder; remove
  example `analysis/example/...` and `data/example/...` paths
- Typical destination: `writting/<manuscript-name>`

### `manuscript_typst`

Use for Typst manuscripts with local artifact pulls.

- Files: `manuscript.typ`, `works.bib`, top-level `Justfile`, and the same
  `artifacts/` layout as `manuscript_simple`
- Entry points: `just artifacts`, `just check-artifacts`, `just bib-to-yaml`,
  `just compile`
- Notes: sample Typst content and bibliography are placeholders and should be
  replaced early
- Typical destination: `writting/<manuscript-name>`

## Known Mismatch To Handle

Examples in `.dat.docs.md` and `config/templates/README.md` still show
manuscript destinations under `manuscripts/...`, but the current repo layout
includes `writting/`. Prefer `writting/<name>` unless the user explicitly wants
a different structure.
