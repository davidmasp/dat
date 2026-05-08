#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["typer>=0.12.0"]
# ///

from __future__ import annotations

import hashlib
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomllib
import typer

app = typer.Typer(help="Manage manuscript-local artifact copies and integrity checks.")


@dataclass(frozen=True)
class ArtifactConfig:
    artifact_name: str
    artifact_path: Path
    file_name: str
    source_input_path: Path
    source_path: Path
    dest_path: Path


@dataclass(frozen=True)
class ArtifactState:
    artifact_name: str
    artifact_path: Path
    file_name: str
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


def parse_config(config_path: Path, source_base: Path | None = None) -> list[ArtifactConfig]:
    data = load_toml(config_path)
    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise typer.BadParameter("`input.toml` must contain a non-empty `[[artifacts]]` array.")

    config_dir = config_path.parent
    source_root = source_base if source_base is not None else config_dir
    seen_artifact_names: set[str] = set()
    files: list[ArtifactConfig] = []

    for idx, artifact in enumerate(artifacts, start=1):
        if not isinstance(artifact, dict):
            raise typer.BadParameter(f"Artifact block #{idx} must be a table.")

        artifact_name = artifact.get("name")
        artifact_path_raw = artifact.get("path")
        artifact_files = artifact.get("files", [])

        if not isinstance(artifact_name, str) or not artifact_name.strip():
            raise typer.BadParameter(f"Artifact block #{idx} is missing a valid `name`.")
        if artifact_name in seen_artifact_names:
            raise typer.BadParameter(f"Duplicate artifact name: `{artifact_name}`.")
        seen_artifact_names.add(artifact_name)

        if not isinstance(artifact_path_raw, str) or not artifact_path_raw.strip():
            raise typer.BadParameter(f"Artifact `{artifact_name}` is missing a valid `path`.")

        artifact_path = (config_dir / artifact_path_raw).resolve()

        if not isinstance(artifact_files, list) or not artifact_files:
            raise typer.BadParameter(
                f"Artifact `{artifact_name}` must define at least one `[[artifacts.files]]`."
            )

        seen_file_names: set[str] = set()
        for fidx, artifact_file in enumerate(artifact_files, start=1):
            if not isinstance(artifact_file, dict):
                raise typer.BadParameter(
                    f"Artifact `{artifact_name}` file #{fidx} must be a table."
                )

            file_name = artifact_file.get("name")
            source_path_raw = artifact_file.get("path")

            if not isinstance(file_name, str) or not file_name.strip():
                raise typer.BadParameter(
                    f"Artifact `{artifact_name}` file #{fidx} is missing a valid `name`."
                )
            if file_name in seen_file_names:
                raise typer.BadParameter(
                    f"Duplicate file name `{file_name}` in artifact `{artifact_name}`."
                )
            seen_file_names.add(file_name)

            if not isinstance(source_path_raw, str) or not source_path_raw.strip():
                raise typer.BadParameter(
                    f"Artifact `{artifact_name}` file `{file_name}` is missing a valid `path`."
                )

            source_input_path = Path(source_path_raw)
            if source_input_path.is_absolute():
                source_path = source_input_path.resolve()
            else:
                source_path = (source_root / source_input_path).resolve()
            ext = source_path.suffix
            if not ext:
                raise typer.BadParameter(
                    "Artifact "
                    f"`{artifact_name}` file `{file_name}` source has no extension: {source_path_raw}"
                )

            dest_path = artifact_path / artifact_name / f"{file_name}{ext}"
            files.append(
                ArtifactConfig(
                    artifact_name=artifact_name,
                    artifact_path=artifact_path,
                    file_name=file_name,
                    source_input_path=source_input_path,
                    source_path=source_path,
                    dest_path=dest_path,
                )
            )

    seen_dest: dict[Path, tuple[str, str]] = {}
    for artifact_file in files:
        if artifact_file.dest_path in seen_dest:
            prior_artifact, prior_file = seen_dest[artifact_file.dest_path]
            raise typer.BadParameter(
                "Destination conflict: "
                f"`{artifact_file.artifact_name}/{artifact_file.file_name}` and "
                f"`{prior_artifact}/{prior_file}` both map to {artifact_file.dest_path}"
            )
        seen_dest[artifact_file.dest_path] = (
            artifact_file.artifact_name,
            artifact_file.file_name,
        )

    return files


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
    rows: list[ArtifactState],
    project_root: Path,
    root: Path | None = None,
) -> None:
    lines: list[str] = []
    grouped: dict[tuple[str, Path], list[ArtifactState]] = {}
    for row in rows:
        grouped.setdefault((row.artifact_name, row.artifact_path), []).append(row)

    for (artifact_name, artifact_path) in sorted(grouped.keys(), key=lambda x: x[0]):
        lines.extend(
            [
                "[[artifacts]]",
                f"name = {_toml_quote(artifact_name)}",
                f"path = {_toml_quote(_rel_or_abs(artifact_path, project_root))}",
                "",
            ]
        )
        for row in sorted(grouped[(artifact_name, artifact_path)], key=lambda r: r.file_name):
            stored_source_path = _prepend_root(row.source_path, root)
            lines.extend(
                [
                    "[[artifacts.files]]",
                    f"name = {_toml_quote(row.file_name)}",
                    f"source_path = {_toml_quote(str(stored_source_path))}",
                    f"local_path = {_toml_quote(_rel_or_abs(row.local_path, project_root))}",
                    f"md5 = {_toml_quote(row.md5)}",
                    "",
                ]
            )

    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def load_state(state_path: Path) -> list[ArtifactState]:
    data = load_toml(state_path)
    artifacts = data.get("artifacts")
    if not isinstance(artifacts, list):
        raise typer.BadParameter("`state.toml` must contain a `[[artifacts]]` array.")

    out: list[ArtifactState] = []
    seen_keys: set[tuple[str, str]] = set()
    for idx, artifact in enumerate(artifacts, start=1):
        if not isinstance(artifact, dict):
            raise typer.BadParameter(f"State artifact block #{idx} must be a table.")

        artifact_name = artifact.get("name")
        artifact_path_raw = artifact.get("path")
        files = artifact.get("files")

        if not isinstance(artifact_name, str):
            raise typer.BadParameter(f"State artifact block #{idx} missing `name`.")
        if not isinstance(artifact_path_raw, str):
            raise typer.BadParameter(f"State artifact `{artifact_name}` missing `path`.")
        if not isinstance(files, list):
            raise typer.BadParameter(f"State artifact `{artifact_name}` missing `files`.")

        artifact_path = Path(artifact_path_raw)

        for fidx, artifact_file in enumerate(files, start=1):
            if not isinstance(artifact_file, dict):
                raise typer.BadParameter(
                    f"State artifact `{artifact_name}` file #{fidx} must be a table."
                )

            name = artifact_file.get("name")
            source = artifact_file.get("source_path")
            local = artifact_file.get("local_path")
            md5 = artifact_file.get("md5")

            if not all(isinstance(v, str) for v in (name, source, local, md5)):
                raise typer.BadParameter(
                    f"State artifact `{artifact_name}` file #{fidx} has invalid fields."
                )
            key = (artifact_name, name)
            if key in seen_keys:
                raise typer.BadParameter(
                    f"Duplicate state artifact entry: {artifact_name}/{name}"
                )
            seen_keys.add(key)

            out.append(
                ArtifactState(
                    artifact_name=artifact_name,
                    artifact_path=artifact_path,
                    file_name=name,
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
        help="Prepend this root folder when resolving source paths from input TOML.",
    ),
) -> None:
    """Copy configured artifacts and update state.toml."""
    config = config.resolve()
    state = state.resolve()
    project_root = config.parent
    if root is not None:
        root = root.expanduser()
        if not root.is_absolute():
            root = (project_root / root).resolve()
        else:
            root = root.resolve()

    artifact_configs = parse_config(config, source_base=root)

    failures: list[str] = []
    state_rows: list[ArtifactState] = []

    for artifact_file in artifact_configs:
        if not artifact_file.source_path.exists():
            failures.append(
                "Missing source for "
                f"{artifact_file.artifact_name}/{artifact_file.file_name}: {artifact_file.source_path}"
            )
            continue
        if not artifact_file.source_path.is_file():
            failures.append(
                "Source is not a file for "
                f"{artifact_file.artifact_name}/{artifact_file.file_name}: {artifact_file.source_path}"
            )
            continue

        artifact_file.dest_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(artifact_file.source_path, artifact_file.dest_path)
            local_md5 = md5sum(artifact_file.dest_path)
        except OSError as exc:
            failures.append(
                f"Copy failed for {artifact_file.artifact_name}/{artifact_file.file_name}: {exc}"
            )
            continue

        typer.echo(
            "copied "
            f"{artifact_file.artifact_name}/{artifact_file.file_name} -> "
            f"{_rel_or_abs(artifact_file.dest_path, project_root)}"
        )
        state_rows.append(
            ArtifactState(
                artifact_name=artifact_file.artifact_name,
                artifact_path=artifact_file.artifact_path,
                file_name=artifact_file.file_name,
                source_path=(
                    artifact_file.source_input_path if root is not None else artifact_file.source_path
                ),
                local_path=artifact_file.dest_path,
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
    expected_index = {(p.artifact_name, p.file_name): p for p in expected}

    if not state.exists():
        typer.echo(f"ERROR: state file not found: {state}", err=True)
        raise typer.Exit(code=1)

    rows = load_state(state)
    state_index = {(r.artifact_name, r.file_name): r for r in rows}

    failures: list[str] = []

    missing_state = sorted(set(expected_index) - set(state_index))
    extra_state = sorted(set(state_index) - set(expected_index))

    for artifact_name, file_name in missing_state:
        failures.append(f"Missing state entry: {artifact_name}/{file_name}")

    for artifact_name, file_name in extra_state:
        failures.append(f"Extra state entry (not in input.toml): {artifact_name}/{file_name}")

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

    typer.echo("All tracked manuscript artifacts are valid.")


if __name__ == "__main__":
    app()
