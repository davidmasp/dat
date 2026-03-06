# Figure panel configuration (`input.toml`)

* `input.toml` defines which panel files are collected into each figure output folder. This is the file where we should define the panels to track.

* `state.toml` defines the current state of the figure import, essentially stores the md5 of the local file, the original full path and the path of the local file. It fills up after copying.

## Structure

- `[[figures]]`: starts a new figure block.
- `name`: logical figure name (used as the figure identifier, must be unique across all figures).
- `path`: base output folder for that figure (for example `./main_figures` or `./supp_figures`).
  Panel files are copied into a subfolder named after the figure: `<path>/<figure_name>/<panel_name>.<ext>`.

Inside each figure block:

- `[[figures.panels]]`: adds one panel entry to that figure (at least one panel is required).
- `path`: path where the panel file is located.
- `name`: name to assign to the panel (must be unique within the figure).

## Minimal example

```toml
[[figures]]
name = "figure01"
path = "./main_figures"

[[figures.panels]]
name = "f1_b"
path = "data/dataSimple/figures/mutationsColon/prefilter_clones_b.pdf"
```

## Typical usage

1. Add or edit a `[[figures]]` block for each output figure set.
2. Add one `[[figures.panels]]` entry per panel file you want in that figure.

3. Run the helper script to copy the figures into the appropriate folders and write/update `state.toml`.

```bash
uv run scripts/figures.py copy
```

To use a custom root folder for panel `path` values in `input.toml` (for both source file lookup and stored `source_path` values in `state.toml`):

```bash
uv run scripts/figures.py copy --root /my/root
```

4. Validate that the figures are the correct version by computing the md5sum of the figure paths

```bash
uv run scripts/figures.py check
```
