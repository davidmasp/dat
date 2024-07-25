# Conda environtments

🚨 Note: The use of conda is discontinued

See this on how to install [miniconda](https://docs.anaconda.com/miniconda/).

Note that to shell-init anaconda you will need to run:

```bash
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
# OR
eval "$(/Users/david.mas/src/miniconda3/bin/conda shell.zsh hook)"
```

Also Note that you may need to re-install the dat package within your conda python installation. See [here](../src/datpy/README.md).

## Usage

To install all environtments locally use:

```bash
dat conda --all -v
```

To install all environtments globally use:

```bash
dat conda --all -v --globally
```

To install only a selected list of environtments run:

```bash
dat conda --envs env1,env2 -v
```

To remove all conda environtments run:

```bash
dat conda --all -v --delete
# or
dat conda --all -v --delete --globally
```

To remove a single conda environtment run

```bash
rm -rf env1
```

## Notes

* If installling globally the name of the environtment is set in the
`yaml` file. If installed locally the name of the folder that contains
the environtment is set to the name of the file without the extension.

