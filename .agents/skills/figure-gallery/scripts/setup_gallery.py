#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Copy the reusable gallery builder, template, and initial legends into an atomic folder."""

import argparse
from pathlib import Path
import shutil


def setup(root: Path) -> list[Path]:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Atomic folder must already exist: {root}")
    skill = Path(__file__).resolve().parents[1]
    copies = {
        root / "scripts/build_figure_gallery.py": skill / "scripts/build_figure_gallery.py",
        root / "scripts/figure_gallery.html": skill / "assets/figure_gallery.html",
    }
    legends = root / "figures.legends.toml"
    for directory in (root / "scripts", root / "figures"):
        if directory.is_symlink() or (directory.exists() and not directory.is_dir()):
            raise ValueError(f"Expected an ordinary directory: {directory}")
    # Preflight before copying; never overwrite local code or authored legends.
    for destination, source in copies.items():
        if destination.is_symlink() or (
            destination.exists() and (
                not destination.is_file() or destination.read_bytes() != source.read_bytes()
            )
        ):
            raise ValueError(f"Existing gallery file differs; inspect and merge it manually: {destination}")
    if legends.is_symlink() or (legends.exists() and not legends.is_file()):
        raise ValueError(f"Expected an ordinary legend file: {legends}")
    copies[legends] = skill / "assets/figures.legends.toml"
    created = []
    for destination, source in copies.items():
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            created.append(destination)
    (root / "figures").mkdir(exist_ok=True)
    return created


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Existing atomic folder")
    args = parser.parse_args()
    try:
        created = setup(args.root)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Gallery setup failed: {error}\n")
    for path in created:
        print(f"Created {path}")
    print("Preserved existing files. Edit figures.legends.toml, then run from the atomic root:")
    print("  uv run scripts/build_figure_gallery.py")


if __name__ == "__main__":
    main()
