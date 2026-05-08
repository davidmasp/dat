template_dir := "config/templates"
template_remote := "template"
template_url := "git@github.com:davidmasp/dat.git"
template_ref := "template/main"
template_sync_branch := "sync/template-updates"

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

# Add the upstream template remote once in a generated project.
template-add-remote url=template_url:
    git remote add {{ template_remote }} "{{ url }}"

# Fetch upstream template changes.
template-fetch:
    git fetch {{ template_remote }}

# Create a sync branch and merge upstream template changes into it.
template-sync branch=template_sync_branch ref=template_ref:
    git fetch {{ template_remote }}
    git checkout -b "{{ branch }}"
    git merge "{{ ref }}" --allow-unrelated-histories
