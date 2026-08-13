# Orderflow — Python metrics validation repository

Retail **order fulfillment** service (FastAPI + SQLAlchemy + SQLite) built to validate Testable’s Python language support, the **103 white-box metrics** in `Testable_Strategy_Metrics_Mapping_v0.2.xlsx`, the tools in `Testable_Language_Version_Matrix_Verbatim_Fixed.xlsx`, database trigger execution, and a **passing Confidence Score**.

This is a real application: catalog, pricing, inventory reservation, payments, fulfillment state machine, invoices, packing slips, and SQL audit triggers. It is not a folder of metric-name stubs.

## Architecture

```
python-testing/
├── src/orderflow/          FastAPI application (orderflow package)
│   ├── main.py             App factory, OpenAPI, lifespan
│   ├── config.py           Environment settings
│   ├── database.py         Engine, SQLite pragmas, SQL triggers
│   ├── models/             Customer, product, order, inventory, audit
│   ├── schemas/            Pydantic request/response contracts
│   ├── repositories/       Persistence (parameterized ORM)
│   ├── services/           Pricing, inventory, fulfillment, payment, documents
│   ├── api/routers/        HTTP adapters (controllers)
│   ├── validators/         Input sanitization and state rules
│   ├── security/           Hashed API keys, access checks
│   ├── analysis/           Risk, control-flow, definition-use helpers
│   └── utils/              Money, hashing, dates
├── infra/terraform/        CIS-aligned AWS IaC (Checkov/tfsec)
├── Dockerfile              Non-root production image
├── tests/unit|integration|functional
├── scripts/                Seed, quality runner, git churn
├── quality/config|reports  Tool configs and generated evidence
├── docs/                   Metric, tool, version, and gate traceability
└── .github/workflows/ci.yml
```

Confidence Engine gate mapping (Performance, Security, IaC, SOC 2, secrets): [docs/gate-coverage.md](docs/gate-coverage.md).

## Supported Python versions

Install and analyse on **3.10, 3.11, 3.12** (CI). The package also classifies **3.13**. Syntax stays on 3.10 so older matrix rows still parse. See [docs/version-compatibility.md](docs/version-compatibility.md).

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -U pip
pip install -e ".[dev]"
# or
pip install -r requirements-dev.txt
pip install -e .
```

## Run the application

```bash
python scripts/seed_demo.py
python -m orderflow.main
```

- API: http://127.0.0.1:8000
- OpenAPI: http://127.0.0.1:8000/openapi.json
- Health: http://127.0.0.1:8000/health

Set the API key in the environment (nothing is hardcoded in source):

```bash
set ORDERFLOW_API_KEY=your-local-key
curl -H "X-API-Key: your-local-key" http://127.0.0.1:8000/customers
```

## Run tests

```bash
pytest
pytest --cov=orderflow --cov-branch --cov-report=term-missing
```

Markers: `unit`, `integration`, `functional`.

## How 103 metrics are covered

Every White Box L5 metric from the mapping workbook is traced to source in [docs/metric-coverage.md](docs/metric-coverage.md).

| Technique | Realistic behaviour in this repo |
|---|---|
| Cyclomatic / cognitive complexity | Nested pricing rules and fulfillment risk classification |
| Duplication | Invoice vs packing-slip builders |
| Lint | flake8 + pylint configs and CI |
| SAST | Sanitizers, hashed keys, ORM (no concatenated SQL) |
| SCA | Pinned `requirements.txt` + pip-audit |
| Statement / branch / path coverage | pytest-cov with branch data; loop 0/1/n and exception paths |
| Mutation | Assertion-heavy pricing tests + mutmut config |
| Coverage delta | CI coverage.xml |
| All-defs / all-uses | Quote arithmetic and `remaining_defs_uses` |
| Code churn | `scripts/git_churn.py` once git history exists |

## How tools are exercised

See [docs/tool-coverage.md](docs/tool-coverage.md). Local bundle:

```bash
python scripts/run_quality_tools.py
```

JSON/text evidence is written under `quality/reports/` so a Testable run can persist results in its database.

## Database triggers

On startup the app creates SQLite triggers (`trg_orders_after_insert`, `trg_orders_after_update`, `trg_inventory_after_update`) that write `audit_events`. Creating or updating an order therefore produces durable audit rows — the same events a pipeline can store after a run.

`GET /health` reports `triggers_installed`.

## Connect to Testable

1. Push this repository to GitHub (keep the default branch, typically `main` or `master`).
2. In Testable, link the GitHub repo (Code → Linked). Link the work item/story as well so Story is not “Not Linked”.
3. Select language **Python** and a supported version (**3.10–3.13**).
4. Point the quality tools at `src/orderflow` (not `.venv`). Enable Coverage.py / pytest-cov, pylint or flake8, Bandit/Semgrep, pip-audit, radon/lizard, jscpd, mutmut/cosmic-ray, and git churn as configured in your org.
5. Execute a Confidence Engine run on the commit you just pushed.

### Expected pipeline behaviour

| Gate | What this repo supplies | Why the previous 58 / Hold failed |
|---|---|---|
| Pipeline | GitHub Actions: pytest, coverage, flake8, bandit, pip-audit, radon | Pipeline was **0** — no CI evidence |
| Whitebox | Analysable 3.10+ source, configs, reports | Partial static score only (29/50) |
| Blackbox | Functional API journeys, boundaries, OpenAPI contract | Blackbox was **0** |

The earlier **58 / 100 Hold** on commit `56b186d` was a static-only score with empty pipeline and blackbox gates. This repository is designed so those gates have real evidence. Testable still computes the number; this project does not fake it.

Linking a story in the Testable UI is required for story-level confidence and is outside the git tree.

## Metric → source → test → execution

Example:

```text
Metric: Execution Path Integrity
Tool: Crosshair / Mccabe / Radon
Source: src/orderflow/services/pricing_service.py
Function: PricingService.quote
Test: tests/unit/test_pricing_service.py
Purpose: Independent pricing paths (tier, volume, promo, shipping, tax)
```

Full table: [docs/metric-coverage.md](docs/metric-coverage.md).

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `ORDERFLOW_DATABASE_URL` | `sqlite:///./data/runtime/orderflow.db` | SQLAlchemy URL |
| `ORDERFLOW_API_KEY` | _(empty — required for mutating routes)_ | API authentication |
| `ORDERFLOW_ENVIRONMENT` | `development` | Runtime label |
| `ORDERFLOW_ENABLE_SQL_TRIGGERS` | `true` | Install audit triggers |

## Known limitations

- Black-box Excel rows that require a browser (visual regression, WCAG, keyboard navigation) are not applicable to this API service. API functional, boundary, and OpenAPI contract rows **are** covered.
- Forward-looking CPython 3.14–3.16 matrix rows are documented, not CI-executed.
- Optional tools (Crosshair, Pymcdc, complexipy, cosmic-ray, jscpd CLI) should be installed in the Testable runner; they are not required to start the API.
- Set `ORDERFLOW_API_KEY` before serving. The application does not ship a default secret.
