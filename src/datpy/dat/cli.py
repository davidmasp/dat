
import click
import os
import json as jspy
import dat.templates as tmp
import dat.figures as fig
from datetime import datetime

import pdb

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command('figures')
@click.option('--config_file','-c',
                default='figures/panels.toml',
                help='Configuration file')
@click.option('--to_path','-t',
                default='figures',
                help='Output path')
@click.option('--overwrite','-o',
                is_flag=True,
                help='Overwrite files')
def cli_figures(config_file, to_path, overwrite):
    fig.figures_wrk(config_file, to_path, overwrite)

@cli.command('template')
@click.option('--list','-l',
              is_flag=True,
              help='List available templates')
@click.option('--root','-i',
              default='../config/templates',
              help='Template folder to use')
@click.option('--template','-t',
              default='data_pipeline',
              help='Template to use')
@click.option('--variables','-v',
              default='name=output',
              help='comma separated string of variables to use')
@click.option('--defaults','-d',
              default='../config/templates/defaults.toml',
              help='comma separated string of variables to use')
@click.option('--output','-o',
              default='dataPipeline',
              help='output directory')
@click.option('--verbose/--quiet', default=False)
def cli_template(list, root, template, variables, defaults, output, verbose):
    if list:
        click.echo(">> Listing available templates")
        templates = os.listdir(root)
        templates = [t for t in templates if os.path.isdir(os.path.join(root, t))]
        for t in templates:
            click.echo(t)
        return
    
    ### check if template is a directory and exists
    template_dir = os.path.join(root, template)
    if os.path.isdir(template_dir):
        if verbose:
            click.echo("Using template folder")
    else:
        raise Exception("Template is not a folder")
    
    ## check if folder name ends in /, maybe there is a better way?
    if template.endswith('/'):
        template = template[:-1]
    
    all_defaults = tmp.read_defaults(defaults)
    # if a variable is in defaults but also in vars it will be overwritten
    if template not in all_defaults:
        raise Exception("Template not found in defaults")
    var_dict = all_defaults[template]
    vars = variables.split(',')
    for v in vars:
        fields = v.split('=')
        var_dict[fields[0]] = fields[1]
    var_dict['today'] = datetime.now().isoformat()

    tmp.create_directory_structure(
        template_dir, output, var_dict
    )

if __name__ == "__main__":
    files = "codes.txt"
