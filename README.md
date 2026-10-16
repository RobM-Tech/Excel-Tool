# Excel-Tool

Python utility that reconciles requirements between a **DOORS export** and a **rubric** of originating requirement IDs.

Built for repeated baseline reconciliations where the workbook layout stays the same.

## Problem

Requirements imported into DOORS are often split across multiple rows that share an Originating ID. Manually comparing the DOORS export to the original rubric is slow and error-prone across successive configurations.

## What it does

Given Excel workbooks for a configuration baseline, the tool writes a **copy** of the DOORS workbook (the original is never modified) and adds:

| Sheet | Description |
|-------|-------------|
| **List One** | Originating IDs in the rubric but not in DOORS (optionally enriched with MASTER IDs; see below) |
| **List Two** | Originating IDs in DOORS but not in the rubric (with DOORS `ID`) |
| **List Three** | DOORS rows that share the same Object Text (excluding `n/a`) |
| **List Four** | DOORS rows where Originating ID contains more than one ID (data-quality flag) |

Multi-value Originating ID cells are split for comparison. Presence means at least one occurrence.

### Optional inputs (current workflow)

Depending on the run, the tool may also accept:

- **MASTER** (e.g. All SDD requirements) — left-join on Originating ID so List One can include associated MCLLR `ID` values when present
- **Helper exports** used only for a **List One post-filter** (interim):
  - Objects with Originating ID not tagged USAF Basic 8.1
  - Objects with Branch Off Of populated  

That post-filter walks branch-off relationships and drops List One Originating IDs that are covered by a related object with exact configuration tag `USAF_BASIC 8.1`. This path is modular and may be removed or replaced when a stable master baseline becomes the primary compare source for later batches.

## Tech stack

- Python 3.12+
- uv + `pyproject.toml`
- pandas
- openpyxl
- pytest
- `src/` layout

## Setup

```bash
git clone https://github.com/RobM-Tech/Excel-Tool.git
cd Excel-Tool
uv sync


## Usage

```bash
uv run python -m excel_tool.main
```

When prompted, drag and drop the DOORS file, then the Rubric file.  
Output is written next to the DOORS file as `*_reconciled.xlsx`.

## Project layout

```text
src/excel_tool/
  main.py
  config/data_config.py
  functions/
    collection.py
    load.py
    compare.py
    write.py
tests/
```

## Design notes

- Original DOORS file is never overwritten
- File roles are explicit (DOORS, RUBRIC, and optional roles as needed)
- Exploded Originating IDs keep the original row index for multi-ID flagging
- Core Rubric ↔ DOORS pipeline is reusable for additional file pairs with the same format
- List One branch coverage filter is isolated so it can be gated or removed without rewriting the core compare

## Status

Block 8.1 reconciliations in progress. Core lists are stable; optional List One coverage filter and MASTER enrichment are under review with the data owner and may change as a master baseline is established for later batches.

## Data

No proprietary requirement text is stored in this repository.