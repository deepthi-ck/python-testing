# Metric coverage mapping

Source: Testable_Strategy_Metrics_Mapping_v0.2.xlsx White Box sheet.

Total mapped metrics: **103**.

| ID | L5 Metric | L3 Technique | Primary tool | Emitted tool | Source | Function / config | Purpose |
|---:|---|---|---|---|---|---|---|
| 001 | Execution Path Integrity | Cyclomatic Complexity | crosshair | Mccabe | src/orderflow/services/pricing_service.py | PricingService.quote | Nested commercial rules create independent execution paths. |
| 002 | Decision Outcome Verification | Cyclomatic Complexity | Coverage.py | Mccabe | src/orderflow/services/pricing_service.py | PricingService.quote | Nested commercial rules create independent execution paths. |
| 003 | Logical Sub-expression Validation | Cyclomatic Complexity | Pymcdc | Mccabe | src/orderflow/services/pricing_service.py | PricingService.quote | Nested commercial rules create independent execution paths. |
| 004 | Total Logical Combinatorial Coverage | Cyclomatic Complexity | Crosshair | Mccabe | src/orderflow/services/pricing_service.py | PricingService.quote | Nested commercial rules create independent execution paths. |
| 005 | Technical Debt Impact | Cyclomatic Complexity | Radon/Lizard | Mccabe | src/orderflow/services/pricing_service.py | PricingService.quote | Nested commercial rules create independent execution paths. |
| 006 | QA Resource Allocation | Cyclomatic Complexity | testmon | Mccabe | src/orderflow/services/pricing_service.py | PricingService.quote | Nested commercial rules create independent execution paths. |
| 007 | Technical Debt Impact | Cognitive Complexity | cognitive-ast | radon_cc | src/orderflow/analysis/risk.py | classify_fulfillment_risk | Deep nested risk classification increases human comprehension load. |
| 008 | Unit Test Complexity | Cognitive Complexity | cognitive-ast | radon_cc | src/orderflow/analysis/risk.py | classify_fulfillment_risk | Deep nested risk classification increases human comprehension load. |
| 009 | Defect Probability | Cognitive Complexity | cognitive-ast | radon_cc | src/orderflow/analysis/risk.py | classify_fulfillment_risk | Deep nested risk classification increases human comprehension load. |
| 010 | Modularization Opportunity | Cognitive Complexity | cognitive-ast | radon_cc | src/orderflow/analysis/risk.py | classify_fulfillment_risk | Deep nested risk classification increases human comprehension load. |
| 011 | Reviewer Fatigue Factor | Cognitive Complexity | cognitive-ast | radon_cc | src/orderflow/analysis/risk.py | classify_fulfillment_risk | Deep nested risk classification increases human comprehension load. |
| 012 | QA Resource Allocation | Cognitive Complexity | cognitive-ast | radon_cc | src/orderflow/analysis/risk.py | classify_fulfillment_risk | Deep nested risk classification increases human comprehension load. |
| 013 | Human Cognitive Load | Cognitive Complexity | cognitive-ast | radon_cc | src/orderflow/analysis/risk.py | classify_fulfillment_risk | Deep nested risk classification increases human comprehension load. |
| 014 | Multi-Point Failure Probability | Code Duplication | jscpd | copydetect | src/orderflow/services/reporting_service.py + packing_service.py | render_invoice / render_packing_slip | Near-duplicate document builders for jscpd/copydetect. |
| 015 | Redundancy Localization | Code Duplication | jscpd | copydetect | src/orderflow/services/reporting_service.py + packing_service.py | render_invoice / render_packing_slip | Near-duplicate document builders for jscpd/copydetect. |
| 016 | Structural Cleanliness Score | Code Duplication | jscpd | copydetect | src/orderflow/services/reporting_service.py + packing_service.py | render_invoice / render_packing_slip | Near-duplicate document builders for jscpd/copydetect. |
| 017 | Test Suite Streamlining | Code Duplication | jscpd | copydetect | src/orderflow/services/reporting_service.py + packing_service.py | render_invoice / render_packing_slip | Near-duplicate document builders for jscpd/copydetect. |
| 018 | Abstraction Potential | Code Duplication | jscpd | copydetect | src/orderflow/services/reporting_service.py + packing_service.py | render_invoice / render_packing_slip | Near-duplicate document builders for jscpd/copydetect. |
| 019 | Regression Focus Mapping | Code Duplication | jscpd | copydetect | src/orderflow/services/reporting_service.py + packing_service.py | render_invoice / render_packing_slip | Near-duplicate document builders for jscpd/copydetect. |
| 020 | Synchronization Verification | Code Duplication | jscpd | copydetect | src/orderflow/services/reporting_service.py + packing_service.py | render_invoice / render_packing_slip | Near-duplicate document builders for jscpd/copydetect. |
| 021 | Violation Density per KLOC | Lint / Rule Violations | pylint | flake8 | src/orderflow (project-wide) + .flake8 + pyproject.toml | flake8 / pylint configs | Style, naming, complexity thresholds, and CI gate. |
| 022 | Resource Waste Identification | Lint / Rule Violations | pylint | flake8 | src/orderflow (project-wide) + .flake8 + pyproject.toml | flake8 / pylint configs | Style, naming, complexity thresholds, and CI gate. |
| 023 | Semantic Consistency Score | Lint / Rule Violations | pylint | flake8 | src/orderflow (project-wide) + .flake8 + pyproject.toml | flake8 / pylint configs | Style, naming, complexity thresholds, and CI gate. |
| 024 | Syntactic Uniformity Score | Lint / Rule Violations | pylint | flake8 | src/orderflow (project-wide) + .flake8 + pyproject.toml | flake8 / pylint configs | Style, naming, complexity thresholds, and CI gate. |
| 025 | Structural Threshold Monitoring | Lint / Rule Violations | pylint | flake8 | src/orderflow (project-wide) + .flake8 + pyproject.toml | flake8 / pylint configs | Style, naming, complexity thresholds, and CI gate. |
| 026 | Impact Prioritization | Lint / Rule Violations | pylint | flake8 | src/orderflow (project-wide) + .flake8 + pyproject.toml | flake8 / pylint configs | Style, naming, complexity thresholds, and CI gate. |
| 027 | Aggregated Risk Assessment | Lint / Rule Violations | pylint | flake8 | src/orderflow (project-wide) + .flake8 + pyproject.toml | flake8 / pylint configs | Style, naming, complexity thresholds, and CI gate. |
| 028 | Accuracy Tuning | Lint / Rule Violations | pylint | flake8 | src/orderflow (project-wide) + .flake8 + pyproject.toml | flake8 / pylint configs | Style, naming, complexity thresholds, and CI gate. |
| 029 | Project-Specific Enforcement | Lint / Rule Violations | pylint | flake8 | src/orderflow (project-wide) + .flake8 + pyproject.toml | flake8 / pylint configs | Style, naming, complexity thresholds, and CI gate. |
| 030 | Environment Standardization | Lint / Rule Violations | pylint | flake8 | src/orderflow (project-wide) + .flake8 + pyproject.toml | flake8 / pylint configs | Style, naming, complexity thresholds, and CI gate. |
| 031 | Automated Gatekeeping | Lint / Rule Violations | pylint | flake8 | src/orderflow (project-wide) + .flake8 + pyproject.toml | flake8 / pylint configs | Style, naming, complexity thresholds, and CI gate. |
| 032 | Quality Audit Trail | Lint / Rule Violations | pylint | flake8 | src/orderflow (project-wide) + .flake8 + pyproject.toml | flake8 / pylint configs | Style, naming, complexity thresholds, and CI gate. |
| 033 | Best Practice Compliance | Static Vulnerabilities (SAST) | Semgrep OSS / + / Bandit | semgrep | src/orderflow/validators/input_sanitizer.py + security/auth.py | sanitize_text / authenticate_request | Input sanitization, hashed API keys, parameterized ORM queries. |
| 034 | Entry Point Sanitization | Static Vulnerabilities (SAST) | Semgrep OSS / + / Bandit | bandit | src/orderflow/validators/input_sanitizer.py + security/auth.py | sanitize_text / authenticate_request | Input sanitization, hashed API keys, parameterized ORM queries. |
| 035 | Sensitive Information Tracking | Static Vulnerabilities (SAST) | Semgrep OSS / + / Bandit | bandit | src/orderflow/validators/input_sanitizer.py + security/auth.py | sanitize_text / authenticate_request | Input sanitization, hashed API keys, parameterized ORM queries. |
| 036 | Access Control Verification | Static Vulnerabilities (SAST) | Semgrep OSS / + / Bandit | bandit | src/orderflow/validators/input_sanitizer.py + security/auth.py | sanitize_text / authenticate_request | Input sanitization, hashed API keys, parameterized ORM queries. |
| 037 | Supply Chain Security | Static Vulnerabilities (SAST) | Semgrep OSS / + / Bandit | semgrep | src/orderflow/validators/input_sanitizer.py + security/auth.py | sanitize_text / authenticate_request | Input sanitization, hashed API keys, parameterized ORM queries. |
| 038 | Regulatory Alignment | Static Vulnerabilities (SAST) | Semgrep OSS / + / Bandit | bandit | src/orderflow/validators/input_sanitizer.py + security/auth.py | sanitize_text / authenticate_request | Input sanitization, hashed API keys, parameterized ORM queries. |
| 039 | Exploit Surface Identification | Static Vulnerabilities (SAST) | Semgrep OSS / + / Bandit | bandit | src/orderflow/validators/input_sanitizer.py + security/auth.py | sanitize_text / authenticate_request | Input sanitization, hashed API keys, parameterized ORM queries. |
| 040 | Hidden Relationship Mapping | Dependency Risk (SCA) | pip-audit | safety | requirements.txt | pip-audit | Pinned dependencies for CVE, license, and freshness scans. |
| 041 | Legal Risk Validation | Dependency Risk (SCA) | pip-audit | safety | requirements.txt | pip-audit | Pinned dependencies for CVE, license, and freshness scans. |
| 042 | Trust Integrity Verification | Dependency Risk (SCA) | pip-audit | safety | requirements.txt | pip-audit | Pinned dependencies for CVE, license, and freshness scans. |
| 043 | Community Vitality Tracking | Dependency Risk (SCA) | pip-audit | safety | requirements.txt | pip-audit | Pinned dependencies for CVE, license, and freshness scans. |
| 044 | Mitigation Effort Ranking | Dependency Risk (SCA) | pip-audit | safety | requirements.txt | pip-audit | Pinned dependencies for CVE, license, and freshness scans. |
| 045 | Real-Time Alerting | Dependency Risk (SCA) | pip-audit | safety | requirements.txt | pip-audit | Pinned dependencies for CVE, license, and freshness scans. |
| 046 | Known CVE Count | Dependency Risk (SCA) | pip-audit | safety | requirements.txt | pip-audit | Pinned dependencies for CVE, license, and freshness scans. |
| 047 | Version Lag Assessment | Dependency Risk (SCA) | pip-audit | safety | requirements.txt | pip-audit | Pinned dependencies for CVE, license, and freshness scans. |
| 048 | Test Case Granularity | Statement Coverage | Coverage.py | pytest-cov | tests/ + src/orderflow | pytest-cov | Unit/integration/functional tests execute statements. |
| 049 | Unreachable Logic Identification | Statement Coverage | Coverage.py | pytest-cov | tests/ + src/orderflow | pytest-cov | Unit/integration/functional tests execute statements. |
| 050 | Coverage Gap Analysis | Statement Coverage | Coverage.py | pytest-cov | tests/ + src/orderflow | pytest-cov | Unit/integration/functional tests execute statements. |
| 051 | Surface-Level Correctness | Statement Coverage | Coverage.py | pytest-cov | tests/ + src/orderflow | pytest-cov | Unit/integration/functional tests execute statements. |
| 052 | Statement Coverage % | Statement Coverage | Coverage.py | pytest-cov | tests/ + src/orderflow | pytest-cov | Unit/integration/functional tests execute statements. |
| 053 | Boolean Accuracy Check | Branch Coverage | Coverage.py | pytest-cov --cov-branch | tests/unit/test_fulfillment_and_flow.py | pytest-cov --cov-branch | True/false forks, loops, and exception branches. |
| 054 | Sequence Integrity Mapping | Branch Coverage | Coverage.py | pytest-cov --cov-branch | tests/unit/test_fulfillment_and_flow.py | pytest-cov --cov-branch | True/false forks, loops, and exception branches. |
| 055 | Iteration Boundary Verification | Branch Coverage | Coverage.py | pytest-cov --cov-branch | tests/unit/test_fulfillment_and_flow.py | pytest-cov --cov-branch | True/false forks, loops, and exception branches. |
| 056 | Boundary Failure Identification | Branch Coverage | Coverage.py | pytest-cov --cov-branch | tests/unit/test_fulfillment_and_flow.py | pytest-cov --cov-branch | True/false forks, loops, and exception branches. |
| 057 | Branch Misdirection Discovery | Branch Coverage | Coverage.py | pytest-cov --cov-branch | tests/unit/test_fulfillment_and_flow.py | pytest-cov --cov-branch | True/false forks, loops, and exception branches. |
| 058 | Decision Coverage Gap Analysis | Branch Coverage | Coverage.py | pytest-cov --cov-branch | tests/unit/test_fulfillment_and_flow.py | pytest-cov --cov-branch | True/false forks, loops, and exception branches. |
| 059 | Branch Coverage % | Branch Coverage | Coverage.py | pytest-cov --cov-branch | tests/unit/test_fulfillment_and_flow.py | pytest-cov --cov-branch | True/false forks, loops, and exception branches. |
| 060 | Full Logic Validation | Path Coverage | Coverage.py | coverage.py + ast paths | src/orderflow/analysis/control_flow.py + tests | nested_predicates / exception_path | Distinct routes including nested, loop, and exception paths. |
| 061 | Path Execution Tracking | Path Coverage | Coverage.py | coverage.py + ast paths | src/orderflow/analysis/control_flow.py + tests | nested_predicates / exception_path | Distinct routes including nested, loop, and exception paths. |
| 062 | Gap Identification | Path Coverage | Coverage.py | coverage.py + ast paths | src/orderflow/analysis/control_flow.py + tests | nested_predicates / exception_path | Distinct routes including nested, loop, and exception paths. |
| 063 | Deep Logic Probing | Path Coverage | Coverage.py | coverage_paths | src/orderflow/analysis/control_flow.py + tests | nested_predicates / exception_path | Distinct routes including nested, loop, and exception paths. |
| 064 | Iterative Route Analysis | Path Coverage | Coverage.py | coverage_paths | src/orderflow/analysis/control_flow.py + tests | nested_predicates / exception_path | Distinct routes including nested, loop, and exception paths. |
| 065 | Ghost Code Discovery | Path Coverage | Coverage.py | coverage_paths | src/orderflow/analysis/control_flow.py + tests | nested_predicates / exception_path | Distinct routes including nested, loop, and exception paths. |
| 066 | Error Flow Verification | Path Coverage | Coverage.py | coverage_paths | src/orderflow/analysis/control_flow.py + tests | nested_predicates / exception_path | Distinct routes including nested, loop, and exception paths. |
| 067 | Cross-Component Mapping | Path Coverage | Coverage.py | coverage_paths | src/orderflow/analysis/control_flow.py + tests | nested_predicates / exception_path | Distinct routes including nested, loop, and exception paths. |
| 068 | Automated Quality Enforcement | Path Coverage | Coverage.py | coverage_paths | src/orderflow/analysis/control_flow.py + tests | nested_predicates / exception_path | Distinct routes including nested, loop, and exception paths. |
| 069 | Path Coverage % | Path Coverage | Coverage.py | coverage.py + ast paths | src/orderflow/analysis/control_flow.py + tests | nested_predicates / exception_path | Distinct routes including nested, loop, and exception paths. |
| 070 | Logic Error Sensitivity | Mutation Score | cosmic-ray | mutmut | tests/unit/test_pricing_service.py | mutmut / cosmic-ray | Strong assertions on discount, shipping, and rejection paths. |
| 071 | Test Rigor Assessment | Mutation Score | cosmic-ray | mutmut | tests/unit/test_pricing_service.py | mutmut / cosmic-ray | Strong assertions on discount, shipping, and rejection paths. |
| 072 | Weak Spot Localization | Mutation Score | cosmic-ray | mutmut | tests/unit/test_pricing_service.py | mutmut / cosmic-ray | Strong assertions on discount, shipping, and rejection paths. |
| 073 | Boundary Mutant Analysis | Mutation Score | cosmic-ray | mutmut | tests/unit/test_pricing_service.py | mutmut / cosmic-ray | Strong assertions on discount, shipping, and rejection paths. |
| 074 | Logic Error Sensitivity | Mutation Score | cosmic-ray | mutmut | tests/unit/test_pricing_service.py | mutmut / cosmic-ray | Strong assertions on discount, shipping, and rejection paths. |
| 075 | Test Rigor Assessment | Mutation Score | cosmic-ray | mutmut | tests/unit/test_pricing_service.py | mutmut / cosmic-ray | Strong assertions on discount, shipping, and rejection paths. |
| 076 | Logic Error Sensitivity | Mutation Score | cosmic-ray | mutmut | tests/unit/test_pricing_service.py | mutmut / cosmic-ray | Strong assertions on discount, shipping, and rejection paths. |
| 077 | Coverage Delta % | Coverage Delta | Coverage.py | coveragepy | .github/workflows/ci.yml + quality/reports/coverage | coverage xml | CI stores coverage.xml for delta against baseline. |
| 078 | Discovery Power Assessment | Coverage Delta | Coverage.py | coveragepy | .github/workflows/ci.yml + quality/reports/coverage | coverage xml | CI stores coverage.xml for delta against baseline. |
| 079 | Deployment Readiness Guard | Coverage Delta | Coverage.py | coveragepy | .github/workflows/ci.yml + quality/reports/coverage | coverage xml | CI stores coverage.xml for delta against baseline. |
| 080 | Ripple Effect Mapping | Coverage Delta | Coverage.py | coveragepy | .github/workflows/ci.yml + quality/reports/coverage | coverage xml | CI stores coverage.xml for delta against baseline. |
| 081 | Fresh Logic Proofing | Coverage Delta | Coverage.py | coveragepy | .github/workflows/ci.yml + quality/reports/coverage | coverage xml | CI stores coverage.xml for delta against baseline. |
| 082 | Structural Health Benchmarking | Coverage Delta | Coverage.py | coveragepy | .github/workflows/ci.yml + quality/reports/coverage | coverage xml | CI stores coverage.xml for delta against baseline. |
| 083 | All-Defs Coverage % | All Definition Coverage | Beniget | pyflakes | src/orderflow/analysis/risk.py | remaining_defs_uses | Totals are defined then used in computation and predicates. |
| 084 | Data Path Correlation | All Definition Coverage | coverage.py | pyflakes | src/orderflow/analysis/risk.py | remaining_defs_uses | Totals are defined then used in computation and predicates. |
| 085 | DU-Path Validation | All Definition Coverage | Beniget | pyflakes | src/orderflow/analysis/risk.py | remaining_defs_uses | Totals are defined then used in computation and predicates. |
| 086 | Dead Data Identification | All Definition Coverage | pylint | pyflakes | src/orderflow/analysis/risk.py | remaining_defs_uses | Totals are defined then used in computation and predicates. |
| 087 | Null and Boundary Flow Analysis | All Definition Coverage | CrossHair | pyflakes | src/orderflow/analysis/risk.py | remaining_defs_uses | Totals are defined then used in computation and predicates. |
| 088 | Audit Trail Verification | All Definition Coverage | pydriller | pyflakes | src/orderflow/analysis/risk.py | remaining_defs_uses | Totals are defined then used in computation and predicates. |
| 089 | Data Processing Validation | All Uses Coverage | coverage.py + beniget | all_uses | src/orderflow/services/pricing_service.py | quote | C-use (arithmetic) and P-use (shipping/tax predicates) on quoted totals. |
| 090 | Logic Influence Assessment | All Uses Coverage | coverage.py + beniget | all_uses | src/orderflow/services/pricing_service.py | quote | C-use (arithmetic) and P-use (shipping/tax predicates) on quoted totals. |
| 091 | Path Correlation Mapping | All Uses Coverage | coverage.py + beniget | all_uses | src/orderflow/services/pricing_service.py | quote | C-use (arithmetic) and P-use (shipping/tax predicates) on quoted totals. |
| 092 | Comprehensive Data Proofing | All Uses Coverage | coverage.py + beniget | all_uses | src/orderflow/services/pricing_service.py | quote | C-use (arithmetic) and P-use (shipping/tax predicates) on quoted totals. |
| 093 | Data Flow Gap Analysis | All Uses Coverage | coverage.py + beniget | all_uses | src/orderflow/services/pricing_service.py | quote | C-use (arithmetic) and P-use (shipping/tax predicates) on quoted totals. |
| 094 | Ambiguity Resolution | All Uses Coverage | coverage.py + beniget | all_uses | src/orderflow/services/pricing_service.py | quote | C-use (arithmetic) and P-use (shipping/tax predicates) on quoted totals. |
| 095 | Inter-procedural Tracking | All Uses Coverage | coverage.py + beniget | all_uses | src/orderflow/services/pricing_service.py | quote | C-use (arithmetic) and P-use (shipping/tax predicates) on quoted totals. |
| 096 | Ghost Use Identification | All Uses Coverage | coverage.py + beniget | all_uses | src/orderflow/services/pricing_service.py | quote | C-use (arithmetic) and P-use (shipping/tax predicates) on quoted totals. |
| 097 | Data Integrity Audit | All Uses Coverage | coverage.py + beniget | all_uses | src/orderflow/services/pricing_service.py | quote | C-use (arithmetic) and P-use (shipping/tax predicates) on quoted totals. |
| 098 | All-Uses Coverage % | All Uses Coverage | coverage.py + beniget | all_uses | src/orderflow/services/pricing_service.py | quote | C-use (arithmetic) and P-use (shipping/tax predicates) on quoted totals. |
| 099 | Code Churn Score | Code Churn | pydriller | git_churn | scripts/git_churn.py | via_git / via_pydriller | Commit add/delete rates after the repository has history. |
| 100 | Impact-Driven Verification | Code Churn | pydriller | git_churn | scripts/git_churn.py | via_git / via_pydriller | Commit add/delete rates after the repository has history. |
| 101 | Fault Probability Modeling | Code Churn | pydriller | git_churn | scripts/git_churn.py | via_git / via_pydriller | Commit add/delete rates after the repository has history. |
| 102 | Validation Suite Updates | Code Churn | pydriller | git_churn | scripts/git_churn.py | via_git / via_pydriller | Commit add/delete rates after the repository has history. |
| 103 | Side Effect Mapping | Code Churn | pydriller | git_churn | scripts/git_churn.py | via_git / via_pydriller | Commit add/delete rates after the repository has history. |
