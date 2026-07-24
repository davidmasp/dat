# Artifact Configuration (`input.toml`)

`input.toml` defines which generated files should be pulled into this
manuscript-local `artifacts/` folder.

`state.toml` stores the copied local paths plus md5 hashes so you can check
whether the local copies still match what was pulled.

## Structure

- `[[artifacts]]`: starts a new artifact block.
- `name`: logical artifact group name, unique within the file.
- `path`: base output folder for that group, for example `./main_artifacts` or
  `./supp_artifacts`.
- `[[artifacts.files]]`: adds one file to the group.
- `name`: local name to assign to the copied file.
- `path`: source path of the generated file to pull.

Copied files land in:

`<path>/<artifact_group>/<file_name>.<ext>`

## Example

```toml
[[artifacts]]
name = "figure01"
path = "./main_artifacts"

[[artifacts.files]]
name = "panel_a"
path = "analysis/example/results/panel_a.pdf"
```

## Usage

```bash
just --justfile artifacts/Justfile copy
just --justfile artifacts/Justfile check
```
