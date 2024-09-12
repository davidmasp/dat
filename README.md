# DAT

Template repository for data analysis projects.

## Usage

### Create a new repo from the template

```bash
gh repo create <name> --clone --private --template davidmasp/dat
cd <name>
git remote add template git@github.com:davidmasp/dat.git
```

### When checking for template updates run

🚨 NOTE: this will create a bunch of merge conflicts for the
files that have been updated, you should accept "current"
changes for the ones that you don't want to be over-written.

```bash
git fetch --all
git merge template/main --allow-unrelated-histories
```

### Install the datpy pacakge (one-time)

```bash
cd src/datpy
pip install .
cd ../..
```

### Create a default folder for data

```bash
cd data
dat template -t data_simple -o dataSimple -v "name=My Data Simple Folder"
```

### Create a new report folder for a quaterly report

```bash
cd reports
dat template -o Q324 --template reports_simple --variables "name=Q324" 
```

### Create a new container folder

```bash
cd containers
dat template -t singularity_py -o test_py -v "name=example2Py,version=0.0.2"
```

### List the available templates with

```bash
dat template --root config/templates -l
```

### Gather relevant panel figures to a central location

This command requires a configuration file (`panels.toml`). This is
by default located in [`figures/panels.toml`](figures/panels.toml), but it
is not required.

```bash
dat figures -o
```

### Build automatically conda environments

See [this](environments/README.md)

### Sync data from a server

We need to set up a config file in the root directory (of the project, for here would be ~/projects/dat) named `.datsync.toml`.
See [this file](.datsync.toml) as example.

```bash
# for files
dat sync file.txt
# for folders
dat sync folder --dot
```

Note that the user needs to be in the same directory as the remote session.

Also note that to sync files in nested directories we need to create the directories locally too.
