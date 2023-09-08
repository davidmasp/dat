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
cd src
./buildpkg.py -p datpy
cd ..
```

### Create a new default data folder

```
cd data
dat template -i ../config/templates/data_template -v 'type=muts;source=SELF;author=DMP' -o ./muts_SELF
```

### Create a new default sandbox folder

```
cd sandbox
dat template -i ../config/templates/sandbox_template -v 'title=earthsize;description=check the size of the earth;author=DMP' -o ./earthsize
```

### Create a new default container folder

```
cd containers
dat template -i ../config/templates/singularitypy_template -v 'name=scikit;author=DM' -o ./scikit
```
