
import click
import os
import json as jspy
import dat.templates as tmp

import pdb

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")

@cli.command('template')
@click.option('--template','-i',
              default='../../templates',
              help='Template folder to use')
@click.option('--json','-f',
              help='json directory with variable names')
@click.option('--variables','-v',
              default='name=output',
              help='string of variables to use')
@click.option('--output','-o',
              default='params.json',
              help='json directory with variable names')
@click.option('--verbose/--quiet', default=False)
def cli_files(template, json, variables, output, verbose):
    ## heck if json argument is given
    if json:
        if verbose:
            click.echo("Using json file, cli variables and defaults will be ignored")
        tmp.render_folder_from_fromJson(var_file = variables,
                                        folder = template,
                                        output_folder = output)
    else:
        ## find defaults files
        template_folder = os.path.dirname(template)
        dft = os.path.join(template_folder, "defaults.json")
        print(dft)
        if os.path.exists(dft):
            with open(dft, "r") as fh:
                defaults = jspy.load(fh)
                ## template base name
        else:
            raise Exception("No defaults.json file found in template folder")
        template_name = os.path.basename(template)
        var_dict = defaults[template_name]
        # repopulate with vars
        variables = variables.split(';')
        for v in variables:
            fields = v.split('=')
            var_dict[fields[0]] = fields[1]
        tmp.render_from_folder(variables = var_dict,
                                folder = template,
                                output_folder = output)

if __name__ == "__main__":
    files = "codes.txt"

