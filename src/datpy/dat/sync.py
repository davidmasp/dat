
import os
import toml
import click
import subprocess

def find_config(cdir, max_depth = 3):
    if max_depth == 0:
        raise Exception("Could not find .datsync.toml")
    files = os.listdir(cdir)
    if ".datsync.toml" in files:
        return os.path.join(cdir, ".datsync.toml")
    else:
        new_path = os.path.dirname(cdir)
        new_depth = max_depth - 1
        return find_config(new_path, new_depth)


## The alias `myrsync` needs to be available in the path. 
# alias myrsync="rsync -avP --copy-links "

def sync_file(target, connection = None, use_dot = False, dry = False):
    working_dir = os.path.realpath(os.getcwd())
    toml_config = find_config(working_dir)
    with open(toml_config, 'r') as f:
        config_base = toml.load(f)
        if connection is not None:
            config = config_base[connection]
        else:
            defa = config_base['default_connection']
            config = config_base[defa]
    localroot = os.path.expanduser(config['localroot'])
    #pdb.set_trace()
    relpath = os.path.relpath(working_dir, localroot)
    host = config['sshhost']
    remote_root = config['remoteroot']
    full_file_path = os.path.join(remote_root, relpath, target)
    hoststr = f"{host}:{full_file_path}"
    base_cmd = [
        "rsync",
        "-avP",
        "--copy-links"
    ]
      
    if use_dot:
        cmd_str = base_cmd + [
            hoststr,
            "."
        ]
    else:
        cmd_str = base_cmd + [
            hoststr,
            target
        ]
    if dry:
        click.echo(" ".join(cmd_str))
        return
    else:
        click.echo(" ".join(cmd_str))
        subprocess.run(" ".join(cmd_str), shell=True, executable="/bin/zsh")





