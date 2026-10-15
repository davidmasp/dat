---
name: just-sync
description: Add rsync recipes to an atomic data or analysis folder's Justfile for laptop–HPC transfers. Use only when explicitly invoked as $just-sync.
---

# Just Sync

Add the requested sync direction and file selection to the current atomic
folder under `data/` or `analysis/`. Follow the Justfile, dotenv, and optional
module conventions in [dat-atomic-folder](../dat-atomic-folder/SKILL.md), keeping
this skill separate from folder scaffolding. Run both directions from the laptop.

## Paths and scope

- Inspect the atomic README, Justfile, and input/output paths. Upload data and
  reference documents that are difficult to obtain on the HPC; download the
  expected `results/`, `figures/`, or `tables/`. Add only requested transfers.
- Reuse the SSH alias and any path override already supplied by the user or
  local configuration; ask only for missing information such as the alias.
- By default, replace the local home prefix with literal `~`, preserving the
  rest of the atomic path: `/Users/david.mas/code/ytb2rss/analysis/qc` maps to
  `~/code/ytb2rss/analysis/qc`. Do not send `/Users/...` or expand the remote
  tilde using the laptop's home. Use a different path only when supplied.
- Assume the remote destination exists. Do not probe it over SSH, run remote
  `mkdir`, or add existence checks.
- Put `HPC_HOST` and `HPC_ATOMIC_PATH` in the atomic `.env` and document them
  in the root Justfile's expected-variable comments. Keep `.env` ignored and
  preserve unrelated values. Add safe examples to `.env.sample`:

```dotenv
HPC_HOST=sshalias
HPC_ATOMIC_PATH=~/code/example-project/analysis/example
```

## Recipes

Keep every rsync command in the form `rsync -avP --copy-links [filters] source
destination`. `--copy-links` deliberately copies symlink targets. A source
directory without a trailing slash copies the directory itself; keep the
destination at its parent to avoid flattening or nesting it twice.

These root Justfile recipes illustrate each direction. Replace `data` with
the actual input directory; add separate commands for reference documents or
other expected output directories only as needed.

```just
# Upload local inputs to the matching atomic folder on the HPC.
sync-to-hpc:
    rsync -avP --copy-links data "${HPC_HOST}:${HPC_ATOMIC_PATH}/"

# Download generated results into this atomic folder.
sync-from-hpc:
    rsync -avP --copy-links "${HPC_HOST}:${HPC_ATOMIC_PATH}/results" .
```

For example, these expand to:

```bash
rsync -avP --copy-links data sshalias:~/code/example-project/analysis/example/
rsync -avP --copy-links sshalias:~/code/example-project/analysis/example/results .
```

Keep a small recipe set in the root Justfile. When there are more than six
recipes and grouping helps, downloads can live in `recipes/sync/justfile` with
`set working-directory := '../..'` at the top. Declare
`mod sync 'recipes/sync/justfile'` in the root and invoke
`just sync::sync-from-hpc`. Keep dotenv loading in the root; modules use the
loaded environment variables rather than assuming root Just variables are shared.

## File selection patterns

Add filters only when requested. Quote globs so the shell does not expand them.
Include directories before file rules to traverse nested topics; the final
exclude rejects other files. Preserve the source-directory and parent-destination
pair from the basic recipes.

```bash
# Download only PNGs, retaining figures/<topic>/... paths.
rsync -avP --copy-links --include '*/' --include '*.png' --exclude '*' "${HPC_HOST}:${HPC_ATOMIC_PATH}/figures" .

# Download PNG and PDF figures together.
rsync -avP --copy-links --include '*/' --include '*.png' --include '*.pdf' --exclude '*' "${HPC_HOST}:${HPC_ATOMIC_PATH}/figures" .

# Upload data while omitting cache directories and temporary files.
rsync -avP --copy-links --exclude 'cache/' --exclude '*.tmp' data "${HPC_HOST}:${HPC_ATOMIC_PATH}/"
```

These include rules can create empty directories; add `--prune-empty-dirs`
when those should be omitted. Avoid remote wildcards for recursive file selection.
Do not add `--delete` unless the user explicitly requests deletion mirroring.

## Finish

Document direction, selected paths/filters, required `.env` values, and invocation
in the atomic README. Check `just --list` and `just --dry-run sync-from-hpc`
(or the actual recipe/module name) from the atomic root. Creating recipes does
not request a transfer: run rsync only when the user asks to sync. Before an
authorized download overwrites existing outputs, check their downstream use.
