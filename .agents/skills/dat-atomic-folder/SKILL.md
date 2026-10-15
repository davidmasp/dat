---
name: dat-atomic-folder
description: Define, create, or review the reproducible structure of an atomic analysis or data folder in a DAT repository. Load only when explicitly requested.
---

# DAT Atomic Folder

Apply these conventions when explicitly loaded. An atomic folder is a mostly
self-contained analysis or data-processing unit under `analysis/` or `data/`.
It may consume another atomic folder's results, but has its own configuration,
commands, scripts, and outputs. Keep changes scoped to the requested folder;
adapting an existing folder does not authorize running its pipeline or moving
outputs used downstream.

## Layout

```text
analysis/<name>/ or data/<name>/
├── README.md
├── Justfile
├── .gitignore
├── .env
├── .env.sample
├── scripts/
├── notebooks/
├── figures/<topic>/
├── tables/<topic>/
├── results/<topic>/
├── main.nf                   # only for a local Nextflow pipeline
├── bin/                      # only for Nextflow executables
├── air.toml                  # when needed
├── pyproject.toml            # when needed
└── recipes/                  # optional; only after exceeding six recipes
```

Create topic directories as outputs are produced. Add conditional files and
directories only when the workflow needs them.

- `Justfile` is the central entrypoint for commands, recipe dependencies, and
  shared workflow variables. Put machine-specific paths and settings in `.env`.
- `scripts/` contains R, Python, and Bash scripts. Their working directory is
  the atomic folder root: use `Rscript scripts/test.R`,
  `uv run scripts/process.py`, or `bash scripts/download.sh` in recipes. Resolve
  relative input and output paths from that root, rather than from `scripts/`.
- `notebooks/` contains notebooks such as marimo Python files and R Markdown.
  Configure execution/rendering to resolve paths from the atomic folder root.
- For a local Nextflow pipeline, keep `main.nf` at the root and put programs
  called by the pipeline in `bin/`. Give each such program a suitable shebang
  and user execute permission (`chmod u+x bin/<program>`), so Nextflow can
  discover and execute it. Ordinary analysis scripts belong in `scripts/`.
- Keep other configuration, such as `nextflow.config`, `air.toml`, or
  `pyproject.toml`, at the root when needed.

## Environment and Justfile

Require the atomic folder's own `.env`; an ancestor's `.env` must not satisfy
this requirement. Start the root `Justfile` with the following pattern, replacing
the example variable comments with the actual expected variables and their
purposes. Put these comments immediately after `set dotenv-load`.

```just
set dotenv-load
# Expected .env variables:
# INPUT_DATA: path to the input dataset on this machine.
# N_THREADS: number of processing threads.
set dotenv-required
set dotenv-path := ".env"

# Enforce local file presence even on versions that fall back to an ancestor.
_local_env := if path_exists(justfile_directory() / ".env") == "true" { "" } else { error("Missing local .env; copy .env.sample to .env and configure it.") }

default:
    @just --list
```

Set `dotenv-path` explicitly and retain the file-presence guard: some Just
versions still fall back to an ancestor when the configured file is missing.
The guard stops recipe execution in that case, including module recipes.
Dotenv values are environment variables: access them as `$INPUT_DATA` in shell recipes,
`Sys.getenv("INPUT_DATA")` in R, or `os.environ["INPUT_DATA"]` in Python.
`dotenv-required` checks file presence; validate required variable values where
they are consumed.

Keep both `.env` and `.env.sample` at the root. The tracked `.env.sample` must
list the relevant variables with phony paths and safe example settings, never
real credentials or private machine paths. Initialize a missing `.env` from
the sample and edit it for the current machine; preserve an existing `.env`.

Include these entries in the atomic folder's `.gitignore`:

```gitignore
/.env
/figures/
/tables/
/results/
```

Keep `.env.sample` trackable, including when broader repository ignore rules
apply. Do not use a blanket `.env*` rule that hides the sample. Outputs must stay
ignored even when a topic folder contains multiple file formats.

Pinned reference: [Just dotenv settings](https://github.com/casey/just#dotenv-settings).

## Output placement

Place generated outputs directly under the root's `figures/`, `tables/`, or
`results/`, grouped by an identifiable analysis topic. A generating script's
name can serve as the topic. For one analysis producing multiple output types,
use the same topic across all three directories, for example
`figures/qc/coverage.png`, `tables/qc/summary.csv`, and
`results/qc/filtered_counts.tsv.gz`. For a complex script covering several
topics, use `<topic>_<subtopic>` consistently across its related outputs.

| Directory | Contents | Preferred formats |
| --- | --- | --- |
| `figures/<topic>/` | Plots, visual analyses, and HTML reports | Appropriate image or HTML format; every PDF plot must also have a PNG alongside it, with the same basename and physical dimensions (choose a suitable PNG DPI). |
| `tables/<topic>/` | Final, human-facing tables produced by scripts | Prefer CSV. These are neither pipeline outputs nor data intended for another program. |
| `results/<topic>/` | Pipeline outputs and data intended as inputs to other scripts or analyses | For R/Python data outputs, prefer compressed TSV (`.tsv.gz`), compressed RDS (`.rds`), or compressed Parquet (`.parquet`). Preserve pipeline-required formats. |

Choose placement by intended use: a CSV that another script consumes belongs
in `results/`. Pipeline outputs belong in `results/`, including tabular outputs.
Create output directories in the generating code or its recipe, so a fresh
checkout can reproduce them.

## Factorizing recipes

Keep recipes in the root `Justfile` until it has more than six recipes. Beyond
that threshold, factor related recipes into modules only when it improves
readability; a `recipes/` folder is optional, not mandatory at recipe seven.

```text
recipes/
├── linting/
│   └── justfile
└── test-data/
    └── justfile
```

Declare these modules in the root `Justfile`:

```just
mod linting 'recipes/linting/justfile'
mod test-data 'recipes/test-data/justfile'
```

Module recipes normally run from the module source directory. Preserve the
atomic-root working directory by starting each of these module justfiles with:

```just
set working-directory := '../..'
```

Invoke them through the root, e.g. `just linting::check`. Keep dotenv loading in
the root; child recipes can use the loaded environment variables. Do not assume
root Just variable definitions are shared with modules.

Pinned reference: [Just modules](https://github.com/casey/just#modules).

## Creating and checking a folder

For a new folder, prefer the repository's existing template workflow. Consult
[`dat-templates`](../dat-templates/SKILL.md), run `just list-templates` from the
repository root, and inspect the smallest suitable starter under
`config/templates/` before copying it.

| Workflow | Starter |
| --- | --- |
| Lightweight data acquisition or preparation | `data_simple` |
| Local Nextflow pipeline | `data_pipeline` |
| Wrapper around an external Nextflow pipeline | `data_external_pipeline` |
| R analysis or figure generation | Adapt `sandbox_simple` under `analysis/<name>`; there is currently no dedicated analysis starter. |

For example, from the repository root:

```bash
just create-from-template data_simple data/my-data
# Or, for an R analysis:
just create-from-template sandbox_simple analysis/my-analysis
```

Refuse an existing destination. Templates are starting points, not guarantees
of compliance with this skill: inspect the copied files, replace placeholders,
add the required local dotenv configuration and ignore rules, and adapt output
paths and recipe commands to the conventions above. Preserve useful pipeline
or analysis code from the starter. Do not modify the shared templates unless
the user also requests that work.

Only when no existing template fits, use the bundled baseline helper:

```bash
uv run .agents/skills/dat-atomic-folder/scripts/scaffold.py analysis/my-analysis
```

The helper refuses an existing destination and creates root files and baseline
directories with example configuration. It does not implement an analysis,
add Nextflow, or factor recipes. Do not run it over a copied template.

Replace the sample variables with the workflow's actual configuration, add
scripts and recipes, and update the atomic `README.md` with inputs, commands,
script purposes, produced artifacts, and their topic paths. For an existing
folder, inspect its README, Justfile, configuration, and downstream consumers
before changing paths.

Verify that recipes run from the atomic root, `.env` is loaded, recipe execution
fails without the local `.env` even if a parent has one, and Git ignores `.env`
and all output directories while allowing `.env.sample`. Check recipe syntax
with `just --list`; only run the actual workflow when it is within the requested
task. Report concrete deviations and reproduction commands in the README and
the response.
