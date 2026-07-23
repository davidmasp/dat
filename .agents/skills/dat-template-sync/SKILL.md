---
name: dat-template-sync
description:
  Update an already initialized DAT-based project from the newest upstream DAT
  template. Use when the user wants to refresh `.dat.docs.md`, copy new starter
  templates, review upstream `config` changes, merge new `Justfile` commands,
  update agent guidance, or copy new repo-local skills from
  `https://github.com/davidmasp/dat` into the current project without
  overwriting project-specific work blindly.
metadata:
  short-description: Update a DAT project from upstream
---

# DAT Template Sync

Update the current project from the upstream DAT template while preserving local
project work.

## Workflow

1. Clone `https://github.com/davidmasp/dat` into a temporary directory using
   `gh repo clone davidmasp/dat <tmp>` if available, otherwise
   `git clone https://github.com/davidmasp/dat <tmp>`.
2. Copy upstream `.dat.docs.md` to the current repo root.
3. Compare upstream `config/templates/` with local `config/templates/`; copy
   templates that do not exist locally.
4. Review the rest of upstream `config/` for useful changes. Apply clearly safe
   additions; ask the user before changing behavior, defaults, profiles, or
   anything likely to affect existing runs.
5. Compare the upstream `Justfile` with the local `Justfile`; add new commands
   without removing or rewriting local commands.
6. Compare upstream `AGENTS.md` with local `AGENTS.md`; merge new guidance that
   applies to DAT projects.
7. Ensure `CLAUDE.md` links to or includes `AGENTS.md` using the repo's existing
   convention.
8. Compare upstream `.agents/skills/` with local `.agents/skills/`; copy skills
   that do not exist locally.
9. Ensure `.codex` and `.claude` link to or expose `.agents/skills` using the
   repo's existing convention. Ask before replacing existing directories or
   symlinks.

## Guardrails

- Treat the current repo as the source of truth for project-specific work.
- Prefer additive changes. Do not overwrite local templates, commands, config,
  or skill edits without comparing first.
- Preserve local formatting where practical; follow upstream structure for newly
  copied files.
- Ask the user when an upstream change is useful but could alter execution
  behavior.
- Finish by showing a concise summary of copied files, merged sections, skipped
  changes, and decisions still waiting on the user.

## Useful Checks

- Run
  `git diff -- .dat.docs.md config Justfile AGENTS.md CLAUDE.md .agents .codex .claude`
  before summarizing.
- Run existing lightweight checks only when they are present and relevant, such
  as `just list-templates`.
