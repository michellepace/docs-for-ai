# Installation and usage


## Installing

Install with [CommonMark](https://spec.commonmark.org/current/) support:

```bash
pipx install mdformat
```

Install with [GitHub Flavored Markdown (GFM)](https://github.github.com/gfm/) support:

```bash
pipx install mdformat
pipx inject mdformat mdformat-gfm
```

Note that GitHub's Markdown renderer supports syntax extensions not included in the GFM specification.
For full GitHub support do:

```bash
pipx install mdformat
pipx inject mdformat mdformat-gfm mdformat-frontmatter mdformat-footnote mdformat-gfm-alerts
```

Install with [Markedly Structured Text (MyST)](https://myst-parser.readthedocs.io/en/latest/using/syntax.html) support:

```bash
pipx install mdformat
pipx inject mdformat mdformat-myst
```

```{warning}
The formatting style produced by mdformat may change in each version.
It is recommended to pin mdformat dependency version.
```

<!-- MANUAL: inlined README.md@1.0.0 'cli-usage' in place of {include}; a refresh reverts this -->

## Command line usage

### Format files

Format files `README.md` and `CHANGELOG.md` in place

```bash
mdformat README.md CHANGELOG.md
```

Format `.md` files in current working directory recursively

```bash
mdformat .
```

Read Markdown from standard input until `EOF`.
Write formatted Markdown to standard output.

```bash
mdformat -
```

### Check formatting

```bash
mdformat --check README.md CHANGELOG.md
```

This will not apply any changes to the files.
If a file is not properly formatted, the exit code will be non-zero.

### Options

```console
foo@bar:~$ mdformat --help
usage: mdformat [-h] [--check] [--no-validate] [--version] [--number]
                [--wrap {keep,no,INTEGER}] [--end-of-line {lf,crlf,keep}]
                [--exclude PATTERN] [--extensions EXTENSION]
                [--codeformatters LANGUAGE]
                [paths ...]

CommonMark compliant Markdown formatter

positional arguments:
  paths                 files to format

options:
  -h, --help            show this help message and exit
  --check               do not apply changes to files
  --no-validate         do not validate that the rendered HTML is consistent
  --version             show program's version number and exit
  --number              apply consecutive numbering to ordered lists
  --wrap {keep,no,INTEGER}
                        paragraph word wrap mode (default: keep)
  --end-of-line {lf,crlf,keep}
                        output file line ending mode (default: lf)
  --exclude PATTERN     exclude files that match the Unix-style glob pattern
                        (multiple allowed)
  --extensions EXTENSION
                        require and enable an extension plugin (multiple
                        allowed) (use `--no-extensions` to disable) (default:
                        all enabled)
  --codeformatters LANGUAGE
                        require and enable a code formatter plugin (multiple
                        allowed) (use `--no-codeformatters` to disable)
                        (default: all enabled)
```

The `--exclude` option is only available on Python 3.13+.

## Python API usage

### Format text

```python
import mdformat

unformatted = "\n\n# A header\n\n"
formatted = mdformat.text(unformatted)
assert formatted == "# A header\n"
```

### Format a file

Format file `README.md` in place:

```python
import mdformat

# Input filepath as a string...
mdformat.file("README.md")

# ...or a pathlib.Path object
import pathlib

filepath = pathlib.Path("README.md")
mdformat.file(filepath)
```

### Options

All formatting style modifying options available in the CLI are also available in the Python API,
with equivalent option names:

```python
import mdformat

mdformat.file(
    "FILENAME.md",
    options={
        "number": True,  # switch on consecutive numbering of ordered lists
        "wrap": 60,  # set word wrap width to 60 characters
    }
)
```

## Usage as a pre-commit hook

`mdformat` can be used as a [pre-commit](https://github.com/pre-commit/pre-commit) hook.
Add the following to your project's `.pre-commit-config.yaml` to enable this:

```yaml
- repo: https://github.com/hukkin/mdformat
  rev: 1.0.0  # Use the ref you want to point at
  hooks:
  - id: mdformat
    # Optionally add plugins
    additional_dependencies:
    - mdformat-gfm
    - mdformat-black
```
