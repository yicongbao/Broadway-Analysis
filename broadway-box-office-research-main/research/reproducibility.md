# Reproducibility

## Environment

Use Python 3.11 or later. A locked direct-dependency environment is listed in `requirements.txt`; package metadata and optional research/test dependencies are defined in `pyproject.toml`.

```bash
python -m venv .venv
python -m pip install -e ".[research,test]"
```

## Authorized source input

The original six-sheet workbook is not distributed because public redistribution rights have not been established. Set `BROADWAY_INPUT_DIR` to a private directory containing the authorized workbook. The loader identifies the analysis sheets by schema and never relies on a public copy of the source filename.

```bash
export BROADWAY_INPUT_DIR=/path/to/authorized/private_inputs
python -m broadway_research.pipeline \
  --input-dir "$BROADWAY_INPUT_DIR" \
  --output-dir .
python -m pytest -q
```

The end-to-end integration test reruns the actual analysis in an isolated temporary directory when `BROADWAY_PRIVATE_INPUT_DIR` is available. In public continuous integration, source-dependent integration coverage is skipped while deterministic tests validate the committed aggregate outputs, executed notebooks, figures, and website assets.

## Notebooks

The five notebooks use `BROADWAY_INPUT_DIR`, load the authorized workbook, and execute data validation, descriptive analysis, production OLS, HC3 inference, diagnostics, sensitivity analysis, and market HAC models. Their committed outputs contain aggregate tables and unlabeled diagnostic figures; no restricted source row is embedded.

## Determinism and publication boundary

The pipeline validates source shapes, benchmark tolerances, missingness, matrix rank, and output JSON before writing public artifacts. It writes only to `results/` and `figures/`, so maintained research prose and the website cannot be overwritten by regeneration. Public dashboard charts use aggregate summaries with small-cell suppression where relevant.
