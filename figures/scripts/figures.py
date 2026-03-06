#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["typer>=0.12.0"]
# ///

from __future__ import annotations

import hashlib
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomllib
import typer

app = typer.Typer(help="Manage figure panel copies and integrity checks.")


@dataclass(frozen=True)
class PanelConfig:
    figure_name: str
    figure_path: Path
    panel_name: str
    source_input_path: Path
    source_path: Path
    dest_path: Path


@dataclass(frozen=True)
class PanelState:
    figure_name: str
    figure_path: Path
    panel_name: str
    source_path: Path
    local_path: Path
    md5: str


def md5sum(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_toml(path: Path) -> dict[str, Any]:
    try:
        with path.open("rb") as fh:
            return tomllib.load(fh)
    except FileNotFoundError:
        raise typer.BadParameter(f"TOML file not found: {path}") from None
    except tomllib.TOMLDecodeError as exc:
        raise typer.BadParameter(f"Invalid TOML in {path}: {exc}") from exc


def parse_config(config_path: Path, source_base: Path | None = None) -> list[PanelConfig]:
    data = load_toml(config_path)
    figures = data.get("figures")
    if not isinstance(figures, list) or not figures:
        raise typer.BadParameter("`input.toml` must contain a non-empty `[[figures]]` array.")

    config_dir = config_path.parent
    source_root = source_base if source_base is not None else config_dir
    seen_figure_names: set[str] = set()
    panels: list[PanelConfig] = []

    for idx, figure in enumerate(figures, start=1):
        if not isinstance(figure, dict):
            raise typer.BadParameter(f"Figure block #{idx} must be a table.")

        figure_name = figure.get("name")
        figure_path_raw = figure.get("path")
        figure_panels = figure.get("panels", [])

        if not isinstance(figure_name, str) or not figure_name.strip():
            raise typer.BadParameter(f"Figure block #{idx} is missing a valid `name`.")
        if figure_name in seen_figure_names:
            raise typer.BadParameter(f"Duplicate figure name: `{figure_name}`.")
        seen_figure_names.add(figure_name)

        if not isinstance(figure_path_raw, str) or not figure_path_raw.strip():
            raise typer.BadParameter(f"Figure `{figure_name}` is missing a valid `path`.")

        figure_path = (config_dir / figure_path_raw).resolve()

        if not isinstance(figure_panels, list) or not figure_panels:
            raise typer.BadParameter(f"Figure `{figure_name}` must define at least one `[[figures.panels]]`.")

        seen_panel_names: set[str] = set()
        for pidx, panel in enumerate(figure_panels, start=1):
            if not isinstance(panel, dict):
                raise typer.BadParameter(
                    f"Figure `{figure_name}` panel #{pidx} must be a table."
                )

            panel_name = panel.get("name")
            source_path_raw = panel.get("path")

            if not isinstance(panel_name, str) or not panel_name.strip():
                raise typer.BadParameter(
                    f"Figure `{figure_name}` panel #{pidx} is missing a valid `name`."
                )
            if panel_name in seen_panel_names:
                raise typer.BadParameter(
                    f"Duplicate panel name `{panel_name}` in figure `{figure_name}`."
                )
            seen_panel_names.add(panel_name)

            if not isinstance(source_path_raw, str) or not source_path_raw.strip():
                raise typer.BadParameter(
                    f"Figure `{figure_name}` panel `{panel_name}` is missing a valid `path`."
                )

            source_input_path = Path(source_path_raw)
            if source_input_path.is_absolute():
                source_path = source_input_path.resolve()
            else:
                source_path = (source_root / source_input_path).resolve()
            ext = source_path.suffix
            if not ext:
                raise typer.BadParameter(
                    f"Figure `{figure_name}` panel `{panel_name}` source has no extension: {source_path_raw}"
                )

            dest_path = figure_path / figure_name / f"{panel_name}{ext}"
            panels.append(
                PanelConfig(
                    figure_name=figure_name,
                    figure_path=figure_path,
                    panel_name=panel_name,
                    source_input_path=source_input_path,
                    source_path=source_path,
                    dest_path=dest_path,
                )
            )

    seen_dest: dict[Path, tuple[str, str]] = {}
    for panel in panels:
        if panel.dest_path in seen_dest:
            prior_figure, prior_panel = seen_dest[panel.dest_path]
            raise typer.BadParameter(
                "Destination conflict: "
                f"`{panel.figure_name}/{panel.panel_name}` and `{prior_figure}/{prior_panel}` "
                f"both map to {panel.dest_path}"
            )
        seen_dest[panel.dest_path] = (panel.figure_name, panel.panel_name)

    return panels


def _rel_or_abs(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def _toml_quote(value: str) -> str:
    return "\"" + value.replace("\\", "\\\\").replace("\"", "\\\"") + "\""


def _prepend_root(path: Path, root: Path | None) -> Path:
    if root is None:
        return path
    if path.is_absolute():
        return root.joinpath(*path.parts[1:])
    return root / path


def write_state(
    state_path: Path,
    rows: list[PanelState],
    project_root: Path,
    root: Path | None = None,
) -> None:
    lines: list[str] = []
    grouped: dict[tuple[str, Path], list[PanelState]] = {}
    for row in rows:
        grouped.setdefault((row.figure_name, row.figure_path), []).append(row)

    for (figure_name, figure_path) in sorted(grouped.keys(), key=lambda x: x[0]):
        lines.extend(
            [
                "[[figures]]",
                f"name = {_toml_quote(figure_name)}",
                f"path = {_toml_quote(_rel_or_abs(figure_path, project_root))}",
                "",
            ]
        )
        for row in sorted(grouped[(figure_name, figure_path)], key=lambda r: r.panel_name):
            stored_source_path = _prepend_root(row.source_path, root)
            lines.extend(
                [
                    "[[figures.panels]]",
                    f"name = {_toml_quote(row.panel_name)}",
                    f"source_path = {_toml_quote(str(stored_source_path))}",
                    f"local_path = {_toml_quote(_rel_or_abs(row.local_path, project_root))}",
                    f"md5 = {_toml_quote(row.md5)}",
                    "",
                ]
            )

    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def load_state(state_path: Path) -> list[PanelState]:
    data = load_toml(state_path)
    figures = data.get("figures")
    if not isinstance(figures, list):
        raise typer.BadParameter("`state.toml` must contain a `[[figures]]` array.")

    out: list[PanelState] = []
    seen_keys: set[tuple[str, str]] = set()
    for idx, figure in enumerate(figures, start=1):
        if not isinstance(figure, dict):
            raise typer.BadParameter(f"State figure block #{idx} must be a table.")

        figure_name = figure.get("name")
        figure_path_raw = figure.get("path")
        panels = figure.get("panels")

        if not isinstance(figure_name, str):
            raise typer.BadParameter(f"State figure block #{idx} missing `name`.")
        if not isinstance(figure_path_raw, str):
            raise typer.BadParameter(f"State figure `{figure_name}` missing `path`.")
        if not isinstance(panels, list):
            raise typer.BadParameter(f"State figure `{figure_name}` missing `panels`.")

        figure_path = Path(figure_path_raw)

        for pidx, panel in enumerate(panels, start=1):
            if not isinstance(panel, dict):
                raise typer.BadParameter(
                    f"State figure `{figure_name}` panel #{pidx} must be a table."
                )

            name = panel.get("name")
            source = panel.get("source_path")
            local = panel.get("local_path")
            md5 = panel.get("md5")

            if not all(isinstance(v, str) for v in (name, source, local, md5)):
                raise typer.BadParameter(
                    f"State figure `{figure_name}` panel #{pidx} has invalid fields."
                )
            key = (figure_name, name)
            if key in seen_keys:
                raise typer.BadParameter(
                    f"Duplicate state panel entry: {figure_name}/{name}"
                )
            seen_keys.add(key)

            out.append(
                PanelState(
                    figure_name=figure_name,
                    figure_path=figure_path,
                    panel_name=name,
                    source_path=Path(source),
                    local_path=Path(local),
                    md5=md5,
                )
            )

    return out


@app.command()
def copy(
    config: Path = typer.Option(Path("input.toml"), "--config", help="Path to input TOML."),
    state: Path = typer.Option(Path("state.toml"), "--state", help="Path to state TOML."),
    root: Path | None = typer.Option(
        None,
        "--root",
        help="Prepend this root folder when writing `source_path` values to state TOML.",
    ),
) -> None:
    """Copy configured panels and update state.toml."""
    config = config.resolve()
    state = state.resolve()
    project_root = config.parent
    if root is not None:
        root = root.expanduser()
        if not root.is_absolute():
            root = (project_root / root).resolve()
        else:
            root = root.resolve()

    panel_configs = parse_config(config, source_base=root)

    failures: list[str] = []
    state_rows: list[PanelState] = []

    for panel in panel_configs:
        if not panel.source_path.exists():
            failures.append(
                f"Missing source for {panel.figure_name}/{panel.panel_name}: {panel.source_path}"
            )
            continue
        if not panel.source_path.is_file():
            failures.append(
                f"Source is not a file for {panel.figure_name}/{panel.panel_name}: {panel.source_path}"
            )
            continue

        panel.dest_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(panel.source_path, panel.dest_path)
            local_md5 = md5sum(panel.dest_path)
        except OSError as exc:
            failures.append(
                f"Copy failed for {panel.figure_name}/{panel.panel_name}: {exc}"
            )
            continue

        typer.echo(
            f"copied {panel.figure_name}/{panel.panel_name} -> {_rel_or_abs(panel.dest_path, project_root)}"
        )
        state_rows.append(
            PanelState(
                figure_name=panel.figure_name,
                figure_path=panel.figure_path,
                panel_name=panel.panel_name,
                source_path=panel.source_input_path if root is not None else panel.source_path,
                local_path=panel.dest_path,
                md5=local_md5,
            )
        )

    if state_rows:
        write_state(state, state_rows, project_root, root=root)
        typer.echo(f"wrote state: {_rel_or_abs(state, project_root)}")

    if failures:
        for msg in failures:
            typer.echo(f"ERROR: {msg}", err=True)
        raise typer.Exit(code=1)


@app.command()
def check(
    config: Path = typer.Option(Path("input.toml"), "--config", help="Path to input TOML."),
    state: Path = typer.Option(Path("state.toml"), "--state", help="Path to state TOML."),
) -> None:
    """Validate local files against state.toml and input.toml."""
    config = config.resolve()
    state = state.resolve()
    project_root = config.parent

    expected = parse_config(config)
    expected_index = {(p.figure_name, p.panel_name): p for p in expected}

    if not state.exists():
        typer.echo(f"ERROR: state file not found: {state}", err=True)
        raise typer.Exit(code=1)

    rows = load_state(state)
    state_index = {(r.figure_name, r.panel_name): r for r in rows}

    failures: list[str] = []

    missing_state = sorted(set(expected_index) - set(state_index))
    extra_state = sorted(set(state_index) - set(expected_index))

    for fig, panel in missing_state:
        failures.append(f"Missing state entry: {fig}/{panel}")

    for fig, panel in extra_state:
        failures.append(f"Extra state entry (not in input.toml): {fig}/{panel}")

    for key in sorted(set(expected_index) & set(state_index)):
        expected_row = expected_index[key]
        state_row = state_index[key]

        local_path = state_row.local_path
        if not local_path.is_absolute():
            local_path = (project_root / local_path).resolve()

        expected_local = expected_row.dest_path
        if local_path != expected_local:
            failures.append(
                f"Local path mismatch for {key[0]}/{key[1]}: state={local_path}, expected={expected_local}"
            )

        if not local_path.exists():
            failures.append(f"Missing local file for {key[0]}/{key[1]}: {local_path}")
            continue
        if not local_path.is_file():
            failures.append(f"Local path is not a file for {key[0]}/{key[1]}: {local_path}")
            continue

        current_md5 = md5sum(local_path)
        if current_md5 != state_row.md5:
            failures.append(
                f"MD5 mismatch for {key[0]}/{key[1]}: state={state_row.md5}, current={current_md5}"
            )
        else:
            typer.echo(f"ok {key[0]}/{key[1]} ({current_md5})")

    if failures:
        for msg in failures:
            typer.echo(f"ERROR: {msg}", err=True)
        raise typer.Exit(code=1)

    typer.echo("All tracked figure panels are valid.")


if __name__ == "__main__":
    app()
