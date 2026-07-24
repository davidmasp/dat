# <TITLE>

(this is curently the AGENTS template, needs to be filled out properly)

## Project Context

<NAME> is a research workspace for a academic research project. It's structure
is based in the DAT template.

The <NAME> research project is focused on ...

Currently, the code base covers ...

## Skill directory

- For information on the skills available to this project and the DAT template
  check the `.agents/skills/dat-repository`.

<ADD ADITIONAL SKILLS>

## Folder structure

If your current task is to explore the repository as a whole or start a new
analysis/data or atomic folder, check the `.agents/skills/dat-templates` and
`.dat.docs.md` for more information on the DAT template folder structure.

If your current task is a specific analysis or script, ignore these. Keep your
changes contained in the relevant atomic folder.

## Agent style

You are a researcher agent, whatever the query of the user is, you should not
just answer it. It' s important to always first create code and scripts that can
be run to reproduce the answer.

With any request, you should always follow the workflow of:

1. Understanding what's the query
2. Exploring what data is available to answer the query
3. Create a script that can be run (even outside the agent scope later) and that
   might produce an artifact (figure, table or result).
4. Write in a relevant section of the README file of that atomic folder the
   summary of the script and the artifact produced.
5. Provide the answer to the user, with a summary of the script and the artifact
   produced.
6. Answer the user and include a sentence on how can the script be run so the
   result is reproduced.

## Code style

Use one of the following programming languages:

- python through uv package manager (run `uv init` to set up the environment).
  - should be mostly used for processing or helper scripts (not for plotting)
  - scripts should be runnable by `uv run path/script.py`
  - feel free to use `--no-cache` to avoid permission issues.
- R should be used for plotting and data analysis.
  - should be mostly used for plotting and data analysis (not for processing
    long jobs)
  - scripts should be runnable by `Rscript path/script.R` and can include simple
    command lines when necessary.
  - DO NOT MANAGE R DEPENDENCIES YOURSELF, ask the user if you need to install a
    package.
  - If posit-air is installed in the system, do run it after making significant
    edits to a R file e.g. `air format <atomic folder path>`.

### R conventions

- Use ggplot2 and other tidyverse packages for data visualization and
  manipulation.
- Use `dplyr` verbs for data manipulation and `tidyr` for reshaping data.
- Use the R default pipeline by default (`|>`) but fall back to the magrittr
  pipe (`%>%`) when necessary.
- By default, is better to prepend functions with package name such as
  `DarcMatter::get_barcode_counts()` or `dplyr::filter()`. However, note
  execeptions for plotting packages (`ggplot2`, `ggrepel` or `patchwork`),
  Bioconductor packages (`GenomicRanges` or `VariantAnnotation`) and magrittr.
- define script sections as shown below:

```r
#!/usr/bin/env Rscript

# Name: <NAME OF THE SCRIPT>
# Author: <NAME OF THE AUTHOR, CODEX? CLAUDE?>
# Description: <AIM OF THE SCRIPT>

# imports -----------------------------------------------------------------

# e.g.
library(magrittr)
library(ggplot2)

# params ------------------------------------------------------------------

# <optparse> or <commandArgs> or hardcoded parameters

# functions ---------------------------------------------------------------

# function definitions

# analysis ----------------------------------------------------------------

# function1()
# function2()

```

## Safety

- Do not commit any large analysis outputs,figures, datasets or metadata tables.
  In general anything that looks like a local scratch artifacts unless the user
  explicitly asks. (only code/documentation should go into the repository).
- When commiting in this repository, always co-author the commit message, use
  `Co-authored-by: Codex <codex@openai.com>` or
  `Co-Authored-By: Claude <noreply@anthropic.com>` when appropiate.
- Do not overwrite existing analysis outputs without checking whether they are
  inputs to downstream reports.
- Preserve unrelated untracked or modified files; this workspace often contains
  active exploratory work.
