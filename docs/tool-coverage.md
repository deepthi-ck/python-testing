# Tool coverage

Primary tools are taken from the **Python** column of `Testable_Strategy_Metrics_Mapping_v0.2.xlsx`. Secondary / emitted tools are the values Testable records in the database.

| Primary tool (Excel) | Emitted / secondary | How this repo exercises it | Config / command |
|---|---|---|---|
| Crosshair | Mccabe | `PricingService.quote` and `classify_fulfillment_risk` expose many independent paths for symbolic / complexity analysis | `python -m crosshair check src/orderflow/services/pricing_service.py` (optional extra) |
| Coverage.py | pytest-cov, coveragepy, coverage_paths | Full pytest suite with branch coverage XML | `pytest --cov=orderflow --cov-branch` |
| Pymcdc | Mccabe | Compound predicates in pricing (`free_shipping_promo or qualifies_threshold or gold_always_free`) and access control | tests in `tests/unit/` |
| Radon / Lizard | Mccabe | Nested pricing, SLA, and risk functions | `python -m radon cc src -s` |
| testmon | Mccabe | Pytest suite is testmon-compatible | `pytest --testmon` (optional extra) |
| cognitive-ast (complexipy) | radon_cc | `classify_fulfillment_risk`, `PricingService._shipping_cents` | `complexipy src` (optional extra) |
| jscpd | copydetect | Near-duplicate invoice vs packing-slip builders | `npx jscpd src/orderflow/services` |
| pylint | flake8 | Project-wide lint + CI gate | `flake8 src` / `pylint src/orderflow` |
| Semgrep OSS + Bandit | semgrep, bandit | Sanitizers, hashed API keys, ORM (no string-built SQL) | `bandit -r src/orderflow` / `semgrep --config quality/config/semgrep.yml` |
| pip-audit | safety | Pinned `requirements.txt` | `pip-audit -r requirements.txt` |
| cosmic-ray | mutmut | Assertion-heavy pricing tests | `mutmut run` |
| Beniget / coverage.py + beniget | pyflakes, all_uses | Definition-use pairs in `remaining_defs_uses` and quote arithmetic | pytest + pyflakes via flake8 |
| pydriller | git_churn | `scripts/git_churn.py` | `python scripts/git_churn.py` |

## Black-box tools (Excel Black Box sheet)

| Tool | What this repo provides |
|---|---|
| Playwright / Selenium (API equivalent) | FastAPI `TestClient` journeys in `tests/functional/` (critical path, happy path, boundaries, OpenAPI contract) |
| Pact / contract | `/openapi.json` is generated from the live app; functional test asserts OpenAPI 3.x and required paths |

## Pipeline tools (Confidence Score)

GitHub Actions (`.github/workflows/ci.yml`) runs tests, coverage, flake8, bandit, pip-audit, and radon on Python 3.10–3.12 so the **Pipeline Gate** is not empty when Testable ingests CI.

Run everything locally:

```bash
python scripts/run_quality_tools.py
```

Reports land in `quality/reports/` for database ingestion.
