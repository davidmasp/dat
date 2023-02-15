
import hashlib
import os
import shutil
import click
import json
import pdb

class Panel(object):
    def __init__(self, folder, file, version, verbose = False):
        self.folder = folder
        self.file = file
        selected_version = version
        available_versions = os.listdir(folder)
        available_versions = [i for i in available_versions if i.startswith("2")]
        for j in available_versions:
            ## check if file exists in this folder
            if not os.path.exists(os.path.join(folder, j, file)):
                available_versions.remove(j)
        if verbose:
            print("Found {} versions.".format(len(available_versions)))
        if selected_version in available_versions:
            self.version = selected_version
        elif selected_version == "latest":
            ## I think this should work because it string sort the ISO
            self.version = max(available_versions)
        else:
            raise ValueError("Version {} not found.".format(selected_version))
        self.full_path = os.path.join(folder, self.version, file)
        if not os.path.exists(self.full_path):
            raise ValueError("File {} not found.".format(self.full_path))
        self.md5 = self.get_md5()
    def get_md5(self):
        md5 = calculate_md5(self.full_path)
        return md5
    def copy_to(self, destination, overwrite = False):
        if not os.path.exists(destination):
            os.mkdir(destination)
        # see https://stackoverflow.com/a/8384786
        head, tail = os.path.split(self.file)
        here_path = os.path.join(destination, tail)
        if os.path.exists(here_path) and overwrite:
            os.remove(here_path)
        elif os.path.exists(here_path) and not overwrite:
            md5_target = calculate_md5(here_path)
            if md5_target == self.md5:
                print("File {} already exists and is up to date.".format(self.file))
            else:
                raise ValueError("File {} already exists.".format(here_path))
        else:
            pass
        ## the 2 is to preserve timestamp
        shutil.copy2(self.full_path, here_path)
            
class Figure(object):
    def __init__(self, name, type, verbose = False):
        self.name = name
        self.verbose = verbose
        self.type = type
        self.folder = os.path.join(self.type, self.name)
        if not os.path.exists(self.type):
            os.mkdir(self.type)
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        self.panels = []
    def add_panel(self, folder, file, version):
        panel_obj = Panel(folder, file, version, verbose = self.verbose)
        self.panels.append(panel_obj)
    def add_panels(self, panels):
        # panels is a array of dicts just as the json
        for panel in panels:
            self.add_panel(panel["path"], panel["fileName"], panel["version"])
    def copy_here(self, overwrite = False):
        if overwrite:
            for panel in self.panels:
                panel.copy_to(self.folder, overwrite = True)
        else:
            for panel in self.panels:
                panel.copy_to(self.folder, overwrite = False)

## see https://stackoverflow.com/a/59056837
def calculate_md5(filename, chunksize = 8192):
    """
    calculate the md5 hash of a file
    """
    with open(filename, "rb") as f:
        file_hash = hashlib.md5()
        chunk = f.read(chunksize)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(chunksize)
    return file_hash.hexdigest()

@click.command()
@click.option('-i','--params', default="panels.json", help='figure parameters.')
@click.option('-o', "--overwrite", is_flag=True, show_default=True, default=False, help="Overwrite current figures.")
def hello(params, overwrite):
    """Simple program that greets NAME for a total of COUNT times."""
    ## read json file
    with open(params, "r") as f:
        figures = json.load(f)
    ## create figures
    for figure in figures:
        figure_obj = Figure(figure["name"], figure["type"], verbose = True)
        figure_obj.add_panels(figure["panels"])
        figure_obj.copy_here(overwrite = overwrite)

if __name__ == '__main__':
    hello()
