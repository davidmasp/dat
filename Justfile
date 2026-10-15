template_dir := "config/templates"
default:
    @just --list

# List available templates under config/templates.
list-templates:
    @find {{ template_dir }} -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort

# Copy a template folder into a destination path relative to the repository root.
create-from-template template_name destination_name:
    template_path="{{ template_dir }}/{{ template_name }}"; \
    if [ ! -d "$template_path" ]; then \
      echo "Unknown template: {{ template_name }}" >&2; \
      echo "Run 'just list-templates' to see available templates." >&2; \
      exit 1; \
    fi; \
    if [ -e "{{ destination_name }}" ]; then \
      echo "Destination already exists: {{ destination_name }}" >&2; \
      exit 1; \
    fi; \
    cp -R "$template_path" "{{ destination_name }}"

# Lint all Markdown files in the repository.
lint-md:
    fd -u -tf -e md . . -x prettier --write --prose-wrap always --print-width 80

# Lint all R files in the repository.
lint-r:
    fd -tf -e R . . -x air format

# Lint all files in the repository.
lint: lint-md lint-r
