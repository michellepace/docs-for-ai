<!-- Source: https://docs.marimo.io/guides/lint_rules/ -->

# Lint Rules

marimo includes a linter that helps you write better notebooks. The linter checks for various issues that could prevent your notebook from running correctly or cause confusion.

## Usage

Run the linter using the CLI:

```bash
# Check all notebooks in current directory
marimo check .

# Check specific files
marimo check notebook1.py notebook2.py

# Auto-fix fixable issues
marimo check --fix .
```

## Rule Categories

marimo's lint rules are organized into three main categories based on their severity:

### 🚨 Breaking Rules

These errors prevent notebook execution.

| Code | Name | Description | Fixable |
| --- | --- | --- | --- |
| [MB001](https://docs.marimo.io/guides/lint_rules/rules/unparsable_cells/) | unparsable-cells | Cell contains unparsable code | ❌ |
| [MB002](https://docs.marimo.io/guides/lint_rules/rules/multiple_definitions/) | multiple-definitions | Multiple cells define the same variable | ❌ |
| [MB003](https://docs.marimo.io/guides/lint_rules/rules/cycle_dependencies/) | cycle-dependencies | Cells have circular dependencies | ❌ |
| [MB004](https://docs.marimo.io/guides/lint_rules/rules/setup_cell_dependencies/) | setup-cell-dependencies | Setup cell cannot have dependencies | ❌ |
| [MB005](https://docs.marimo.io/guides/lint_rules/rules/invalid_syntax/) | invalid-syntax | Cell contains code that throws a SyntaxError on compilation | ❌ |

### ⚠️ Runtime Rules

These issues may cause runtime problems.

| Code | Name | Description | Fixable |
| --- | --- | --- | --- |
| [MR001](https://docs.marimo.io/guides/lint_rules/rules/self_import/) | self-import | Importing a module with the same name as the file | ❌ |
| [MR002](https://docs.marimo.io/guides/lint_rules/rules/branch_expression/) | branch-expression | Branch statements with output expressions that won't be displayed | ❌ |
| [MR003](https://docs.marimo.io/guides/lint_rules/rules/reusable_definition_order/) | reusable-definition-order | Reusable definitions depending on later reusable definitions | ⚠️ |

### ✨ Formatting Rules

These are style and formatting issues.

| Code | Name | Description | Fixable |
| --- | --- | --- | --- |
| [MF001](https://docs.marimo.io/guides/lint_rules/rules/general_formatting/) | general-formatting | General formatting issues with the notebook format. | 🛠️ |
| [MF002](https://docs.marimo.io/guides/lint_rules/rules/parse_stdout/) | parse-stdout | Parse captured stdout during notebook loading | ❌ |
| [MF003](https://docs.marimo.io/guides/lint_rules/rules/parse_stderr/) | parse-stderr | Parse captured stderr during notebook loading | ❌ |
| [MF004](https://docs.marimo.io/guides/lint_rules/rules/empty_cells/) | empty-cells | Empty cells that can be safely removed. | ⚠️ |
| [MF005](https://docs.marimo.io/guides/lint_rules/rules/sql_parse_error/) | sql-parse-error | SQL parsing errors during dependency analysis | ❌ |
| [MF006](https://docs.marimo.io/guides/lint_rules/rules/misc_log_capture/) | misc-log-capture | Miscellaneous log messages during processing | ❌ |
| [MF007](https://docs.marimo.io/guides/lint_rules/rules/markdown_indentation/) | markdown-indentation | Markdown cells in `mo.md()` should be properly indented. | 🛠️ |

## Legend

- 🛠️ = Automatically fixable with `marimo check --fix`
- ⚠️ = Fixable with `marimo check --fix --unsafe-fixes` (may change code behavior)
- ❌ = Not automatically fixable

## Configuration

Most lint rules are enabled by default. You can configure the linter behavior through marimo's configuration system.

## Related Documentation

- [Understanding Errors](https://docs.marimo.io/guides/understanding_errors/) - Detailed explanations of common marimo errors
- [CLI Reference](https://docs.marimo.io/cli/) - Complete CLI documentation including `marimo check`