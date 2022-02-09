# Conda environtments

Directory that contains required conda environtments.

## Usage

To install all environtments locally use:

```bash
./buildenv.py --all -v
```

To install all environtments globally use:

```bash
./buildenv.py --all -v --globally
```

To install only a selected list of environtments run:

```bash
./buildenv.py --envs env1,env2 -v
```

To remove all conda environtments run:

```bash
./buildenv.py --all -v --delete
# or
./buildenv.py --all -v --delete --globally
```

To remove a single conda environtment run

```bash
rm -rf env1
```

## Notes

* If installling globally the name of the environtment is set in the
`yaml` file. If installed locally the name of the folder that contains
the environtment is set to the name of the file without the extension.

