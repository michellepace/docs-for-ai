ContentsMenuExpandLight modeDark modeAuto light/dark, in light modeAuto light/dark, in dark mode[Skip to content](https://mdformat.readthedocs.io/en/stable/users/configuration_file.html#furo-main-content)

[Back to top](https://mdformat.readthedocs.io/en/stable/users/configuration_file.html#)

[View this page](https://mdformat.readthedocs.io/en/stable/_sources/users/configuration_file.md.txt "View this page")

Toggle Light / Dark / Auto color theme

Toggle table of contents sidebar

# Configuration file [¶](https://mdformat.readthedocs.io/en/stable/users/configuration_file.html\#configuration-file "Link to this heading")

Mdformat allows configuration in a [TOML](https://toml.io/) file named `.mdformat.toml`.

The configuration file will be resolved starting from the location of the file being formatted,
and searching up the file tree until a config file is (or isn’t) found.
When formatting standard input stream, resolution will be started from current working directory.

Command line interface arguments take precedence over the configuration file.

## Example configuration [¶](https://mdformat.readthedocs.io/en/stable/users/configuration_file.html\#example-configuration "Link to this heading")

```
# .mdformat.toml
#
# This file shows the default values and is equivalent to having
# no configuration file at all. Change the values for non-default
# behavior.
#
wrap = "keep"         # options: {"keep", "no", INTEGER}
number = false        # options: {false, true}
end_of_line = "lf"    # options: {"lf", "crlf", "keep"}
validate = true       # options: {false, true}
# extensions = [      # options: a list of enabled extensions (default: all installed are enabled)\
#     "gfm",\
#     "toc",\
# ]
# codeformatters = [  # options: a list of enabled code formatter languages (default: all installed are enabled)\
#     "python",\
#     "json",\
# ]

# Python 3.13+ only:
exclude = []          # options: a list of file path pattern strings
```

## Exclude patterns [¶](https://mdformat.readthedocs.io/en/stable/users/configuration_file.html\#exclude-patterns "Link to this heading")

A list of file exclusion patterns can be defined on Python 3.13+.
Unix-style glob patterns are supported, see
[Python’s documentation](https://docs.python.org/3/library/pathlib.html#pattern-language)
for syntax definition.

Glob patterns are matched against relative paths.
If `--exclude` is used on the command line, the paths are relative to current working directory.
Else the paths are relative to the parent directory of the file’s `.mdformat.toml`.

Only files (recursively) contained by the base directory can be excluded.

Files that match an exclusion pattern are _always_ excluded,
even in the case that they are directly referenced in a command line invocation.

### Example patterns [¶](https://mdformat.readthedocs.io/en/stable/users/configuration_file.html\#example-patterns "Link to this heading")

```
# .mdformat.toml
exclude = [\
    # exclude a single root level file\
    "CHANGELOG.md",\
\
    # recursively exclude a root level directory\
    "venv/**",\
\
    # recursively exclude a directory at any level\
    "**/node_modules/**",\
\
    # exclude all .txt files\
    "**/*.txt",\
\
    # exclude all files that are not suffixed .md\
    "**/?", "**/??", "**/???", "**/*[!.]??", "**/*[!m]?", "**/*[!d]",\
]
```

Versions[latest](https://mdformat.readthedocs.io/en/latest/users/configuration_file.html)**[stable](https://mdformat.readthedocs.io/en/stable/users/configuration_file.html)**On Read the Docs[Project Home](https://app.readthedocs.org/projects/mdformat/?utm_source=mdformat&utm_content=flyout)[Builds](https://app.readthedocs.org/projects/mdformat/builds/?utm_source=mdformat&utm_content=flyout)Search

* * *

[Addons documentation](https://docs.readthedocs.io/page/addons.html?utm_source=mdformat&utm_content=flyout) ― Hosted by
[Read the Docs](https://about.readthedocs.com/?utm_source=mdformat&utm_content=flyout)