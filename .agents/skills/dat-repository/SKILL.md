---
name: dat-repository
description:
  General skill to help with DAT repository tasks. Use when the user is asking
  about the DAT template repository in general or when the user is confused on
  how the repository and the project are structured.
metadata:
  short-description: Overall information for a DAT-derived repo.
---

# DAT Repository

Use this skill for general DAT repository questions that are not better handled
by a narrower DAT skill.

If this skill is present in a project, the project was generated from the DAT
template repository: `https://github.com/davidmasp/dat`.

Before explaining or changing the project structure, read `.dat.docs.md` from
the repository root.

## Related Skills

- Use `.agents/skills/dat-template-sync` when the user wants to update this
  project from the newest DAT template.
- Use `.agents/skills/dat-templates` when the user wants to create a new
  template-based `data`, `analysis`, `metadata`, `models`, `sandbox`, or
  `writting` folder.
- Use `.agents/skills/dat-main-readme` when the user wants to update the
  current repository's top-level `README.md`.
