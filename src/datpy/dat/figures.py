
import hashlib
import os
import shutil
from pydantic import BaseModel
from typing import List, Dict, Optional
import toml
import hashlib

import pdb

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

class Panel(BaseModel):
    paths: Dict[str, str]
    versions: List[str]
    desired_version: str
    local_name: str

class Figure(BaseModel):
    panels: List[Panel]
    name: str
    path: str

def figures_wrk(config_file, to_path, overwrite):
    with open(config_file, "r") as f:
        config = toml.load(f)
    figures = []
    for fig in config["figures"]:
        panels_figs = fig.pop("panels")
        panels = []
        for pnl in panels_figs:
            pnl_main_path = os.path.join( pnl["root"], pnl["path"] )
            versions = os.listdir(pnl_main_path)
            versions.sort()
            if pnl["version"] == "latest":
                des_version = versions[-1]
            else:
                des_version = pnl["version"]
            full_paths = [os.path.join(pnl_main_path, i, pnl["fileName"] ) for i in versions]
            local_fn = pnl["localFileName"] if "localFileName" in pnl else pnl["fileName"]
            pnl_obj = Panel(paths = dict(zip(versions, full_paths)),
                            versions = versions,
                            desired_version = des_version,
                            local_name = local_fn)
            panels.append(pnl_obj)
        fig_path = os.path.join(to_path, fig["path"])
        fig_obj = Figure(panels = panels, path = fig_path, name = fig["name"])
        figures.append(fig_obj)
    print(f"total of {len(figures)} figures")
    for i in figures:
        os.makedirs(os.path.join(i.path, i.name), exist_ok=True)
        for j in i.panels:
            path = j.paths[j.desired_version]
            head, tail = os.path.split(path)
            dest_path = os.path.join(i.path, i.name, j.local_name)
            if os.path.exists(dest_path):
                print(f"file {dest_path} already exists")
                source_md5 = calculate_md5(path)
                target_md5 = calculate_md5(dest_path)
                if source_md5 == target_md5:
                    print(f"file {dest_path} is up to date")
                else:
                    if overwrite:
                        print(f"file {dest_path} is outdated, overwriting")
                        shutil.copy2(path, dest_path)
                    else:
                        raise ValueError(f"file {dest_path} is outdated, not overwriting")
            else:
                shutil.copy2(path, dest_path)


