#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Create a new atomic folder without overwriting an existing destination."""

import argparse
from pathlib import Path


JUSTFILE = '''set dotenv-load
# Expected .env variables (replace with the workflow's actual variables):
# INPUT_DATA: path to the input dataset on this machine.
# N_THREADS: number of processing threads.
set dotenv-required
set dotenv-path := ".env"

# Enforce local file presence even on versions that fall back to an ancestor.
_local_env := if path_exists(justfile_directory() / ".env") == "true" { "" } else { error("Missing local .env; copy .env.sample to .env and configure it.") }

default:
    @just --list
'''

ENV_SAMPLE = """# Example values: replace in .env for this machine.
INPUT_DATA=/phony/path/to/input.tsv.gz
N_THREADS=1
"""

GITIGNORE = """/.env
/figures/
/tables/
/results/
"""

README = """# {name}

## Purpose and inputs

Describe this analysis or data-processing unit and its input datasets here.

## Reproduce

This baseline was generated with `dat-atomic-folder/scripts/scaffold.py`.
It creates the root configuration and the scripts, notebooks, and output folders.
Edit `.env` for this machine using `.env.sample` as the configuration reference.
From this atomic folder's root, run `just --list` to see available commands.
Add workflow recipes to `Justfile` and document the command sequence here.

## Scripts and artifacts

Document each script's purpose, its recipe, and the artifacts it produces here.
Use matching topic names under `figures/`, `tables/`, and `results/` for related
outputs. Human-facing script tables belong in `tables/`; pipeline outputs and
data for downstream programs belong in `results/`. All three folders are ignored
by Git. Generated plot PDFs also need matching PNGs at the same physical size.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="New analysis/<name> or data/<name> folder")
    args = parser.parse_args()
    destination = args.destination
    try:
        destination.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        parser.error(f"destination already exists: {destination}")

    for directory in ("scripts", "notebooks", "figures", "tables", "results"):
        (destination / directory).mkdir()
    files = {
        "Justfile": JUSTFILE,
        ".gitignore": GITIGNORE,
        ".env.sample": ENV_SAMPLE,
        ".env": ENV_SAMPLE,
        "README.md": README.format(name=destination.name),
    }
    for name, content in files.items():
        (destination / name).write_text(content, encoding="utf-8")
    print(f"Created {destination}. Edit .env and add workflow scripts and recipes.")


if __name__ == "__main__":
    main()
