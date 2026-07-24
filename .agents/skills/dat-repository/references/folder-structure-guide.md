# Folder structure guide

Shared elements:

- If not stated otherwise, all folders should follow a `snake_case` naming
  convention.

## `./src` - Source code

This folder should include custom packages or re-usable code that is specially
designed for this project, or needed within this project specifically. Any
package in this folder is meant to be installable.

Examples are:

- custom R packages with API interactions
- custom uv tools to retrieve or process data

### Folder structure

The folder structure should follow the atomic subfolder structure. Meaning that
each package or tool should live in a subfolder named accordingly and should be
independently installable.

## `./writting` - Writting

This folder should include all permanent writting that is not code or data. This
includes but is not limited to:

- Manuscripts
- Presentations
- Reports
- Grant proposals

Note that documentation should not be included as it will be stored in each
corresponding atomic folder. For example, documentation for the analysis about X
should be stored in analysis/X/README.md or if more extensive use
analysis/X/docs/README.md.

### Folder structure

Folders in this directory should follow the atomic subfolder structure. Meaning
that each manuscript, slides or artifact should live in a subfolder named
accordingly.

Note that it would be preferable to prefix the subfolder with the date and the
type of artifact.

Note that some templates exist in the config folder that are appropiate for this
folder. For example `config/templates/manuscript_typst` or
`config/templates/manuscript_simple`

## `./sandbox` - Sandbox

Use this directory for temporary analyses, drafts, and experiments that are not
ready to be published in their current form.

### Folder structure

Note that each subfolder should be a separate mini-analysis. Folders at these
stage are not expected to be fully reproducible or documented.

Note that is preferable to prefix the subfolder name with the date.

## `./models` - Models

This folder aims at storing code to train, design and evaluate predictive
models. It might include package-style code when necessary, but the main goal is
to obtain, train or use a predictive model.

### Folder structure

Note that each model should contain its own subfolder, this means, a given
architecture or type of model (not a different set of hyperparameters). Each
subfolder should contain the code to train, evaluate and use the model.

Note that it is preferable, for any kind of model to use snakecase for the
subfolder name. For example, `rf_banana` or `xgboost_pineapple`. The first
element should be the type of model and the second element should be a
descriptive name for the model.

Note that trained model files (e.g., `.pkl`, `.h5`, `.pt`) require careful
handling and should never be commited raw in the repo.

Note that most of the documentation for each model should live in the README
file of a given subfolder. For example, the documentation for the `rf_banana`
model should be in `models/rf_banana/README.md`. If more extensive documentation
is needed, a `docs` subfolder can be created within the model subfolder.

## `./metadata` - Metadata

The metadata folder is meant to store any external or internal metadata that is
used in the project. It might also include small scripts or code to process or
generate metadata. An example is if the raw metadata source is stored in a xlsx
file, a script to export the relevant sheets in csv format might be included.

### Folder structure

Note that for small pieces of metadata that do not contain sensitive
information, (like general knowledge information or publicly available data), it
is preferable to store them in the repository, if the size is small. For
example, a csv file with the list of drug annotations or a genetic code.

If the metadata file is large, contains sensitive information, or is not meant
to be available in the repository, keep the source as external or flagged by the
.gitignore file. In these cases, to check for metadata reproducibility, a `md5`
checksum file might be commited. Include then a rule in the Justfile to check
and create given checksum.

## `./data` - Data

Use this directory for atomic folders that aim at producing or processing data.

This can include:

- Self contained nextflow pipelines that produce data from raw data.
- Data collection scripts that download and process to some minimal level.
- Runs of externally provided nextflow pipelines that produce data.

### Folder structure

Note that subfolders should contain the processed data in a folder named
`results`, other artifacts might be locally produced in subfolders like
`figures` or `tables`. These folders should always be included in the
`.gitignore` file.

The `results` folder should contain the final processed data, ready to be used
in downstream analyses.

Note that a helper Justfile should be included, with commands to run (name of
the recipe should be `run`), clean (name of the recipe should be `clean`) and
test in a small datasetr (name of the recipe should be `test-run`).

## `./analysis` - Analysis

Use this directory for complete, publication-ready analyses. These should be
fully reproducible and docuemented.

### Folder structure

The analysis subfolder should be to some extent, atomic, as in contain witin a
specific topic, figure or panel.

The main structure for an analysis folder should be:

```bash
my_analysis/
├─ scripts/
│  ├─ run_analysis.R
│  ├─ run_analysis.py
├─ figures/
│  ├─ concept1/
│  │  ├─ sample_x.png
│  │  ├─ sample_x_table.csv
│  │  ├─ sample_x.pdf
│  ├─ concept2/
│  │  ├─ sample_x.png
│  │  ├─ sample_x_table.csv
│  │  ├─ sample_x.pdf
├─ tables/
│  ├─ concept2/
│  │  ├─ aggregate.csv
├─ .gitignore
├─ README.md
├─ Justfile
```

Note that:

- scripts should
  - be stored in a `scripts` folder, and should be named according to the
    analysis they perform.
  - be runable from the atomic folder root directory, this normally means
    Rscript ./scripts/run_analysis.R or uv run ./scripts/run_analysis.py
- figures should
  - be stored in a `figures` folder, and should be named according to the
    analysis they represent. If they include different samples, they should also
    contain the sample id in a extra subfolder or in the name of the file.
  - each figure should be normally in png and pdf format, with an additional
    table (stored in csv) that contains the raw data used to generate the data
    (literally the values that are being plotted).
- tables should
  - be stored in the `tables` folder, and should be named according to the
    analysis they represent.
  - It's better to store aggregate tables instead of per sample tables.
  - Summary tables should also be stored in here.
  - Prefer csv when possible.
- The Justfile should:
  - contain recipes to run each of the scripts/analysis. These should have the
    form: run-analysis1, run-analysis2, etc.
  - There should be a catch all recipe (name run) that runs all of the analysis
    sequentially.
- The `.gitignore` file should include figures, tables.
