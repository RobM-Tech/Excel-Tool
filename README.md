# Excel-Tool

Python utility that supports data reconciliations and rubric builds for requirements baselines.

Built for repeated baseline reconciliations where the workbook layout stays the same.

## Problem

Comparing DOORS exports to baseline rubrics or system design documents is slow and error-prone across successive configurations.

## Workflows
The utility detects the mode based on which files are provided during the CLI prompts.

### 1. Set-diff reconcile (List One / List Two)

Compares MCLLR ID between a DOORS export and a rubric to find gaps.

| Sheet | Meaning |
|-------|---------|
| **List One** | In rubric, not in DOORS |
| **List Two** | In DOORS, not in rubric |

**Execution:**
```bash
uv run python -m excel_tool.main
```
When prompted: drop DOORS, drop rubric, leave SDD empty (Enter).

### 2. Build next rubric from SDD

Starts from a Block rubric (e.g. 8.1.1) and an SDD requirements list to build an updated rubric:
- Rows like `Delete - MCLLRnnnn` tag matching IDs on the rubric with a Delete flag.
- Rows that are plain MCLLRs are added if they are not already on the rubric.
- SDD deletes that are not on the starting rubric are output to a separate sheet.

**Execution:**
```bash
uv run python -m excel_tool.main
```
When prompted: leave DOORS empty, drop rubric, drop SDD.

**Output sheets:**
- `Rec_Rubric`
- `Not in Rubric`

## Tech stack

- Python 3.12+
- uv + `pyproject.toml`
- pandas
- openpyxl
- pytest
- `src/` layout

## Setup

```bash
git clone https://github.com
cd Excel-Tool
uv sync
```

## Project layout

```text
src/excel_tool/
  main.py                # CLI prompts and mode selection
  config/data_config.py  # column names, File_data
  functions/
    collection.py        # paths, copy, light helpers
    load.py
    write.py
    reconcile.py         # set_diff_reconcile, run_build_rubric
    compare.py           # List 3 helper retained for later use
tests/
```

## Design notes

- Original files are never overwritten; writes use a copy prefixed as `*_reconciled.xlsx`.
- File roles are explicit (DOORS, RUBRIC, etc.).
- Join key for current workflows is ID (MCLLR), not Originating ID.
- Originating-ID mapping, branch-off filters, and related paths were removed from the live tool after product confirmation.
- List 3 (duplicate Object Text, excluding n/a) is kept in code for a future request; it is not run by default.

## Status

v0.2.0 — set-diff and rubric-build paths in use; OID-centric pipeline retired from the default tool.

## Data

No proprietary requirement text is stored in this repository.