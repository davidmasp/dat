#!/usr/bin/env python

import subprocess
import click
import os

@click.command()
@click.option('-p', '--pkgs', default=None, help = 'Comma separated list of packages to build.')
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.option('-u', '--user', is_flag=True, help='Enables non-root mode for pip')
@click.option('-a', '--all', is_flag=True, help='Builds all packages.')
def hello(pkgs, verbose, all, user):
    """Simple program that builds conda environtments using the shell."""
    current_dir = os.getcwd()
    if all:
        if pkgs is not None:
            raise ValueError('Cannot specify both --all and --pkgs')
        pkgs_files_raw = os.listdir('.')
        pkgs_files = [f for f in pkgs_files_raw if os.path.isdir(f)]
    else:
        pkgs_files = pkgs.split(',')
    if verbose:
        click.echo('Total pkgs found: {}'.format(len(pkgs_files)))
    for pkg in pkgs_files:
        if verbose:
            click.echo('Building pkg: {}'.format(pkg))
        os.chdir(pkg)
        if os.path.isdir("R"):
            if verbose:
                click.echo('R package detected: {}'.format(pkg))
            subprocess.run(["R", "CMD", "INSTALL", "--no-multiarch","--with-keep.source", "."])
        else:
            if verbose:
                click.echo('Python package detected: {}'.format(pkg))
            if user:
                subprocess.run(["pip", "install", "--user", "."])
            else:
                subprocess.run(["pip", "install", "."])
        os.chdir(current_dir)


if __name__ == '__main__':
    hello()

