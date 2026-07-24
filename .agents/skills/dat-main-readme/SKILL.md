---
name: dat-main-readme
description:
  Draft or revise the top-level README for a DAT-based repository. Use when the
  user wants to create, rewrite, or tighten the main project README, especially
  for a new repo with template text, a work-in-progress analysis repo that needs
  a clearer project overview, or a mature repo that should summarize outputs,
  structure, and current status accurately.
metadata:
  short-description: Draft or refresh the main DAT README
---

# DAT Main README

Write the repository's main `README.md` for the current stage of the project,
not for an abstract ideal version of the repo.

In case the AGENTS.md file is still in template form, query the user for the
missing project-specific facts that cannot be inferred from the repo and fill it
out.

## Workflow

1. Read the current `README.md` and `.dat.docs.md` before proposing structure or
   text.
2. Determine the repo stage from the existing README and surrounding files.

Repo stages:

- `just started`: little more than template text or a bare scaffold
- `work in progress`: active code and folders exist, but outputs are still
  evolving
- `final artifacts in preparation`: figures, reports, or manuscripts are being
  assembled
- `published and archived`: the repo mostly documents stable outputs and reuse

3. Ask only for the missing project-specific facts that cannot be inferred from
   the repo, such as the research question, audience, data source names, or
   publication status.

Store inferred or user-provided facts in `.project.facts.md` for future runs,
then summarize the most relevant facts briefly in the README.

4. Rewrite the README to match the detected stage instead of forcing sections
   that are not yet true.
5. Summarize the repo structure briefly using `.dat.docs.md`, but keep the
   README focused on this project's actual contents.
6. Add a link to the DAT template repository:
   `https://github.com/davidmasp/dat`.

## Writing Rules

- Prefer a concise project overview, current status, and practical navigation
  over generic boilerplate. DO NOT ADD boilerplate.
- For early-stage repos, explain intent and planned structure without pretending
  the work is finished. In these cases, do not include a link to any code.
- For later-stage repos, after the summary section, we should include:

Later-stage README sections:

- Add a "Usage" section that explains the repo structure, highlights examples
  from the current project, and shows how to navigate and reproduce the work.
- Add a "Research outputs" section from the `writting/` folder. Include only
  finished outputs; ask the user when completion status is unclear.
- For published or archived repos, include a publication link or DOI. Ask the
  user if it is not available in the repo.
- Mention DAT conventions only insofar as they help a reader navigate this
  specific repository.

## Recommended README Shape

- Title and one-paragraph overview before any top level section
- Current status or project stage as a shield or badge
- Link back to the DAT template repo

Status badges:

- `just started`:
  `![just started](https://img.shields.io/badge/status-just%20started-lightgrey)`
- `work in progress`:
  `![work in progress](https://img.shields.io/badge/status-work%20in%20progress-yellow)`
- `final artifacts in preparation`:
  `![final artifacts in preparation](https://img.shields.io/badge/status-final%20artifacts%20in%20preparation-blue)`
- `published and archived`:
  `![published and archived](https://img.shields.io/badge/status-published%20and%20archived-green)`

## DAT Structure Notes

- Link to `.dat.docs.md` to explain the purpose of folders such as `data/`,
  `analysis/`, `metadata/`, `models/`, `sandbox/`, and `writting/`.
- Translate that structure into plain language; do not paste long taxonomy dumps
  into the README.
