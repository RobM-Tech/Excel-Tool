# Excel-Tool

Python utility that reconciles requirements between a **DOORS export** and a **rubric** of originating requirement IDs.

Built for repeated baseline reconciliations where the workbook layout stays the same.

## Problem

Requirements imported into DOORS are often split across multiple rows that share an Originating ID. Manually comparing the DOORS export to the original rubric is slow and error-prone across successive configurations.

## What it does

Given two Excel workbooks:

1. **DOORS export** — `ID`, `Object Text`, `Originating ID`
2. **Rubric** — column of originating requirement IDs

the tool writes a **copy** of the DOORS workbook (the original is never modified) and adds:

| Sheet | Description |
|-------|-------------|
| **List One** | Originating IDs in the rubric but not in DOORS |
| **List Two** | Originating IDs in DOORS but not in the rubric (with DOORS `ID`) |
| **List Three** | DOORS rows that share the same Object Text (excluding `n/a`) |
| **List Four** | DOORS rows where Originating ID contains more than one ID (data-quality flag) |

Multi-value Originating ID cells are split for comparison. Presence means at least one occurrence.

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
