# DAT

Template repository for data analysis projects.

## Usage

### Create a new repo from the template

```bash
gh repo create <name> --clone --private --template davidmasp/dat
cd <name>
git checkout -b template
git checkout main
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

### List the available templates with

```bash
dat template --root config/templates -l
```

### Gather relevant panels to a central location

This command requires a configuration file (`panels.toml`). This is
by default located in [`figures/panels.toml`](figures/panels.toml), but it
is not required.

```bash
dat figures -o
```

### Sync data from a server

(WIP)

