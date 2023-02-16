

## import jinja and os
from jinja2 import Environment, FileSystemLoader
import os
import json
import pdb

def render_from_file(envir, file_path, variables, output_path):
    """
    Render a jinja template from a file path
    """
    template = envir.get_template(os.path.basename(file_path))
    out_template = template.render(variables)
    with open(output_path, "w") as fh:
        fh.write(out_template)

def render_file_name(envir, file_name, variables):
    if file_name.endswith(".jinja"):
        file_name = file_name[:-6]
    tmpl = envir.from_string(file_name)
    return tmpl.render(variables)

def render_from_folder(variables, folder, output_folder):
    """
    Render a jinja template from a folder path
    """
    # create output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        print("Output folder already exists. Exiting.")
        exit()
        ##make jinja environment
    
    env = Environment(loader=FileSystemLoader(folder))
    templates_list = env.list_templates()
    for ti in templates_list:
        ## render file name
        oname = render_file_name(env, ti, variables)
        oname2 = os.path.join(output_folder, os.path.basename(oname))
        render_from_file(env, ti, variables, oname2)
    return True

def render_folder_from_fromJson(var_file, folder, output_folder):
    ## load var dict from default json file
    with open(var_file, "r") as fh:
        var_dict = json.load(fh)
    current_dict = var_dict[folder]

# =============================
# PARAMS
