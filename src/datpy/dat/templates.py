

## import jinja and os
from jinja2 import Environment, FileSystemLoader
import os
import json
import pdb

import toml

def create_directory_structure(template_dir, output_dir, context):
    """
    This function takes a template dir and creates a new directory structure
    based on the information in context.

        * `template_dir`: The directory containing the template structure
        * `output_dir`: The directory where the new structure will be created
        * `context`: A dictionary containing variables to be used in rendering
    
    The structure of the template directory should looks like this:

    ```
    template/
    ├── {{project_name}}/
    │   ├── src/
    │   │   └── main.py
    │   ├── tests/
    │   │   └── test_main.py
    │   └── README.md
    └── LICENSE
    ```
    """
    # Create Jinja2 environment
    env = Environment(loader=FileSystemLoader(template_dir))
    # Walk through the template directory
    for root, dirs, files in os.walk(template_dir):
        # Create relative path
        rel_path = os.path.relpath(root, template_dir)
        # Render the path using Jinja2
        rendered_path = env.from_string(rel_path).render(context)
        # Create the directory in the output
        os.makedirs(os.path.join(output_dir, rendered_path), exist_ok=True)
        # Process files
        for file in files:
            # Render the filename
            rendered_filename = env.from_string(file).render(context)
            
            # Read and render the file content
            template = env.get_template(os.path.join(rel_path, file))
            rendered_content = template.render(context)
            
            # Write the rendered content to the output file
            output_file_path = os.path.join(output_dir, rendered_path, rendered_filename)
            with open(output_file_path, 'w') as f:
                f.write(rendered_content)

def read_defaults(defaults_file):
    """
    Read the defaults file and return the content as a dictionary.
    """
    with open(defaults_file, 'r') as f:
        defaults = toml.load(f)
    return defaults
