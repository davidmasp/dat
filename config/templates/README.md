# Templates

Directory with starter folders for project sections such as sandbox,
data, manuscripts, and containers.

## Usage

These templates are plain files and are meant to be copied with the
repository `just` rules. Run commands from the repository root, then edit
placeholders directly in the copied files.

### Example

```bash
just list-templates
just create-from-template data_simple data/my_data_source
just create-from-template sandbox_simple sandbox/my_exploratory_analysis
just create-from-template manuscript_simple manuscripts/my_new_manuscript
just create-from-template manuscript_typst manuscripts/my_new_typst_manuscript
```
