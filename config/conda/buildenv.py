#!/usr/bin/env python

import subprocess
import click
import os

@click.command()
@click.option('-g', '--globally' ,is_flag=True, help='Install envs globally')
@click.option('-e', '--envs', default=None, help = 'Comma separated list of environments to build.')
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.option('-a', '--all', is_flag=True, help='Builds all environtments.')
@click.option('-d', '--delete', is_flag=True, help='Deletes all environtments.')
def hello(globally, envs, verbose, all, delete):
    """Simple program that builds conda environtments using the shell."""
    if all:
        if envs is not None:
            raise ValueError('Cannot specify both --all and --envs')
        envs_files_raw = os.listdir('.')
        envs_files = [f for f in envs_files_raw if f.endswith('.yml')]
    else:
        envs_files_raw = envs.split(',')
        envs_files = ["{}.yml".format(f) for f in envs_files_raw]
    if verbose:
        click.echo('Total envs found: {}'.format(len(envs_files)))
    if delete:
        if verbose:
            click.echo('Deleting all envs!')
        print(envs_files)
        for env in envs_files:
            if globally:
                env_name = env.split('.')[0]
                subprocess.run(['conda', 'env', 'remove', '--name', env_name, '-y'])
            else:
                env_name = env.split('.')[0]
                env_name2 = "./{}".format(env_name)
                subprocess.run(['conda', 'env', 'remove', '-p', env_name2, '-y'])
    else:
        for env in envs_files:
            if verbose:
                click.echo('Building env: {}'.format(env))
            if globally:
                subprocess.run(["conda", "env", "create", "-f", env])
            else:
                env_name = env.split('.')[0]
                env_name2 = "./{}".format(env_name)
                subprocess.run(["conda", "env", "create", "-f", env, "--prefix", env_name2])

if __name__ == '__main__':
    hello()
