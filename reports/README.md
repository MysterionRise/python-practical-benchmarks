# Benchmark Reports

Reports in this directory are generated from `run_all_tests.py` JSON output. They are portfolio evidence for reproducibility and benchmark coverage, not universal performance rankings.

## Generate Reports

```bash
make bench-json
make bench-report
```

Equivalent direct commands:

```bash
.venv/bin/python run_all_tests.py --all --quick --format json --output reports/output/quick-results.json
.venv/bin/python scripts/render_report.py reports/output/quick-results.json --output reports/output/quick-summary.md
```

`reports/output/` is ignored because it is local generated output. `reports/samples/` contains committed sample evidence from one machine and should be regenerated when the runner or report renderer changes materially.

## Read Results Carefully

Every report includes environment metadata: Python version, platform, CPU count, git SHA, timestamp, quick mode, measured runs, and warmups. Use those fields before comparing numbers across machines or commits.
