ContentsMenuExpandLight modeDark modeAuto light/dark, in light modeAuto light/dark, in dark mode[Skip to content](https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html#furo-main-content)

[Back to top](https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html#)

[View this page](https://mdformat.readthedocs.io/en/stable/_sources/users/installation_and_usage.md.txt "View this page")

Toggle Light / Dark / Auto color theme

Toggle table of contents sidebar

# Installation and usage [¶](https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html\#installation-and-usage "Link to this heading")

## Installing [¶](https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html\#installing "Link to this heading")

Install with [CommonMark](https://spec.commonmark.org/current/) support:

```
pipx install mdformat
```

Install with [GitHub Flavored Markdown (GFM)](https://github.github.com/gfm/) support:

```
pipx install mdformat
pipx inject mdformat mdformat-gfm
```

Note that GitHub’s Markdown renderer supports syntax extensions not included in the GFM specification.
For full GitHub support do:

```
pipx install mdformat
pipx inject mdformat mdformat-gfm mdformat-frontmatter mdformat-footnote mdformat-gfm-alerts
```

Install with [Markedly Structured Text (MyST)](https://myst-parser.readthedocs.io/en/latest/using/syntax.html) support:

```
pipx install mdformat
pipx inject mdformat mdformat-myst
```

Warning

The formatting style produced by mdformat may change in each version.
It is recommended to pin mdformat dependency version.

## Command line usage [¶](https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html\#command-line-usage "Link to this heading")

### Format files [¶](https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html\#format-files "Link to this heading")

Format files `README.md` and `CHANGELOG.md` in place

```
mdformat README.md CHANGELOG.md
```

Format `.md` files in current working directory recursively

```
mdformat .
```

Read Markdown from standard input until `EOF`.
Write formatted Markdown to standard output.

```
mdformat -
```

### Check formatting [¶](https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html\#check-formatting "Link to this heading")

```
mdformat --check README.md CHANGELOG.md
```

This will not apply any changes to the files.
If a file is not properly formatted, the exit code will be non-zero.

### Options [¶](https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html\#options "Link to this heading")

```
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

## Python API usage [¶](https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html\#python-api-usage "Link to this heading")

### Format text [¶](https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html\#format-text "Link to this heading")

```
import mdformat

unformatted = "\n\n# A header\n\n"
formatted = mdformat.text(unformatted)
assert formatted == "# A header\n"
```

### Format a file [¶](https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html\#format-a-file "Link to this heading")

Format file `README.md` in place:

```
import mdformat

# Input filepath as a string...
mdformat.file("README.md")

# ...or a pathlib.Path object
import pathlib

filepath = pathlib.Path("README.md")
mdformat.file(filepath)
```

### Options [¶](https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html\#id1 "Link to this heading")

All formatting style modifying options available in the CLI are also available in the Python API,
with equivalent option names:

```
import mdformat

mdformat.file(
    "FILENAME.md",
    options={
        "number": True,  # switch on consecutive numbering of ordered lists
        "wrap": 60,  # set word wrap width to 60 characters
    }
)
```

## Usage as a pre-commit hook [¶](https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html\#usage-as-a-pre-commit-hook "Link to this heading")

`mdformat` can be used as a [pre-commit](https://github.com/pre-commit/pre-commit) hook.
Add the following to your project’s `.pre-commit-config.yaml` to enable this:

```
- repo: https://github.com/hukkin/mdformat
  rev: 1.0.0  # Use the ref you want to point at
  hooks:
  - id: mdformat
    # Optionally add plugins
    additional_dependencies:
    - mdformat-gfm
    - mdformat-black
```

Versions[latest](https://mdformat.readthedocs.io/en/latest/users/installation_and_usage.html)**[stable](https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html)**On Read the Docs[Project Home](https://app.readthedocs.org/projects/mdformat/?utm_source=mdformat&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/mdformat/builds/?utm_source=mdformat&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=mdformat&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=mdformat&utm_content=flyout)