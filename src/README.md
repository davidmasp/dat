# Source

Directory to store relevant local developed packages for the current project.

## Usage

Only packages in python and R are supported atm.

### Creating a R package

```R
usethis::create_package("./testR")
```

### Creating a python package

```bash
# conda install -c conda-forge cookiecutter
# might be other versions
cookiecutter gh:TezRomacH/python-package-template --checkout v1.1.1
```

### Installing packages locally

Once you have a minimal version of your packages in this
directory you can install all of them using:

```bash
./buildpkg.py --all -v
```
