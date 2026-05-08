# DAT

Template repository for data analysis projects.

See [CHANGELOG.md](CHANGELOG.md) for a history of changes.

## Usage

### Create a new repo from the template

```bash
gh repo create <name> --clone --private --template davidmasp/dat
cd <name>
just template-add-remote
```

`just template-add-remote` defaults to `git@github.com:davidmasp/dat.git`.
Pass a different URL if the template lives somewhere else:

```bash
just template-add-remote git@github.com:org/template-repo.git
```

### Sync template updates

Start from a clean working tree. The sync happens on a temporary branch so
template conflicts can be reviewed before merging into your project branch.

```bash
just template-sync
```

This runs the same workflow as:

```bash
git fetch template
git checkout -b sync/template-updates
git merge template/main --allow-unrelated-histories
```

Resolve any conflicts, commit the merge, test the project, then merge
`sync/template-updates` into your main project branch. Keep your project version
of files when you have intentionally diverged from the template.

### List available templates

```bash
just list-templates
```

Current starter folders include:

- `data_external_pipeline`
- `data_pipeline`
- `data_simple`
- `manuscript_simple`
- `manuscript_typst`
- `sandbox_simple`

### Create project folders from templates

Copy a template into a destination path relative to the repository root:

```bash
just create-from-template <template-name> <destination-path>
```

For example:

```bash
just create-from-template data_simple data/my_data_source
just create-from-template data_pipeline data/my_pipeline
just create-from-template sandbox_simple sandbox/my_exploratory_analysis
just create-from-template manuscript_simple manuscripts/my_manuscript
just create-from-template manuscript_typst manuscripts/my_typst_manuscript
```

After copying, edit placeholders and local settings directly in the copied
folder.

### Gather figure panels

The figure workflow is configured by [`figures/input.toml`](figures/input.toml).
Each panel copy writes checksum state to `figures/state.toml`.

```bash
just --justfile figures/Justfile copy
just --justfile figures/Justfile check
```

You can also run these from inside `figures/`:

```bash
cd figures
just copy
just check
```

### Manuscripts and reports

Use `manuscripts/` for manuscript-specific folders created from the manuscript
templates. Use `reports/` for text-based reports, preferably Typst documents.
See [`reports/README.md`](reports/README.md) for the shared-report workflow.

### Nextflow configuration

Reusable Nextflow profile snippets live in [`config/nextflow`](config/nextflow),
including local, HPC, Slurm, SGE, conda, micromamba, Apptainer, and Tower
configuration files.
