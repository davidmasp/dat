
# Reports

This folder works as a working directory for multiple
reports derived from the current work.

Reports in this folder should be only "text" based so either
be in markdown format, latex or (preferably) using [typst]().

## Using typst

### Compile all documents

To compile all the reports at once you can run:

```bash
find . -maxdepth 2 -iname "*.typ" -exec typst compile --root .. {} \;
```

(if using modular text, you can benefit of expanding the find command as)

```bash
find . -maxdepth 2 -iname "*.typ" -not -path "./main_*" -exec typst compile --root .. {} \;
```

### Modular text

This will find all the typst main files within
all subfolders and compile them. Because the
root of the project is set one directory down
this allow for re-use of other typst scripts
within the folder. For instance, I can write
only one material and methods for a specific
analysis and place it in `main_MM/analysis1.typ`
and then use the same file in multiple manuscripts
or quarterly reports. To include a document use:

```typst
// text

#include "../main_MM/analysis1.typ"

// text

```

Note that this implies that all the documents
are by definition living documents. That might
be a good or a bad thing. Use relases or commits
to lock specific text versions.


### Shared bibliography

Similar to the "main" module files we can also use
a shared bibliography. The recomended case is to
populate one in the reports root directory
and keep that updated. See file [works.yaml](./works.yaml)
for an example. This file can be referenced inside a report
by doing something like this:

```
// text

This @harry HP novel ...

#bibliography("../works.yaml")
// text
```

Note that this file uses the [Hayagriva](https://github.com/typst/hayagriva/blob/main/docs/file-format.md) developed by typst but should be easily convertible by:


