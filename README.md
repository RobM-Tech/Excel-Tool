# excel-tool

A focused Python utility for reconciling requirements data between two Excel workbooks (a DOORS export and a rubric of originating requirements).

## Problem

When requirements are imported into a requirements-management system they are often split into multiple component rows that share the same originating identifier. Manually comparing the system export against the original rubric is time-consuming and error-prone, especially across repeated configuration baselines.

## What it does

Given two workbooks it produces three clear result sheets inside the DOORS workbook:

1. Originating IDs present in the rubric but missing from the DOORS export  
2. Originating IDs present in the DOORS export but absent from the rubric  
3. Rows inside the DOORS export that share identical Object Text (excluding n/a values)

The tool is designed to be reused across multiple similar reconciliation jobs that share the same overall format.

## Tech stack

- Python 3.12+
- uv + pyproject.toml for environment and dependency management
- pandas for data comparison
- openpyxl for reading/writing Excel structure and adding result sheets
- src layout

## Current status

Early project scaffolding. Core reconciliation logic and CLI are not yet implemented. This repository currently contains only the project structure and documentation.

## Design goals

- Correct handling of duplicate Originating IDs (presence = at least one occurrence)
- Clean separation between data loading, comparison, and output writing
- Minimal configuration changes required for subsequent similar jobs
- No proprietary requirement text stored in the repository
