# GrokBots: The Hidden Cost Experiments

**Allegorise · v1.0**

An exploratory, single-account observational study of AI agent overhead, conducted on 24 November 2026. Reproduce the empirical cost model and deterministic invoice extraction; live AI usage is not guaranteed repeatable. Modeled costs are not actual incremental charges or official xAI prices.

## Reproduce locally

From the repository root with Python 3.13 (tested):

```sh
python -m pip install -r requirements.txt
python scripts/reproduce_costs.py
python scripts/accounting_processor.py data/tokenlab_emails.csv reproduced.csv reproduced_exceptions.csv
python -m unittest discover -s tests -v
```

Expected: 391 calibration rows, 74 selected events, 39 test groups, 9 invoice records, 54 matching fields, zero exceptions. The accounting script only creates an exceptions file when exceptions exist; use a fresh output directory. No API credentials or LLM calls are needed.

## Documentation

- [Methodology and results](docs/methodology.md)
- [Data provenance and publication audit](docs/data_provenance.md)
- [Data dictionary](docs/data_dictionary.md)
- [Experiment index](docs/experiments.md)
- [Change history](CHANGELOG.md)
- [Code license](LICENSE) and [data/documentation license](DATA_LICENSE.md)

Public extracts are derived from private billing evidence, which is not distributed. Synthetic emails are fictional. Exact timestamps retain residual linkage risk. No peer review or xAI endorsement is implied. Cite Allegorise, *GrokBots: The Hidden Cost Experiments*, v1.0. Repository: https://github.com/Allegorise/grokbots-hidden-cost-experiments . Website: https://allegorise.cz . No DOI has been assigned.

**Publication decisions:** the founder approved publication of the complete research dataset, including historical calibration charges and exact UTC timestamps, and accepted the residual contractual-disclosure and timestamp-correlation risks. Infographics are not part of this release. Unresolved attribution and prompt limitations remain as documented in the methodology.
