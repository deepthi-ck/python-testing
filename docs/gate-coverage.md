# Confidence Engine gate mapping

These files exist so Testable can **run** the same static gates shown in the Confidence Engine UI and record PASS when the patterns are clean.

## Performance → Static Analysis

| Gate | What Testable measures | How this repo passes |
|---|---|---|
| Algorithmic Complexity | Lizard CC > 15; nested loops ≥ 3 | Pricing and risk logic is O(n), one loop deep, CC kept ≤ 15 |
| Database Query Analysis | ORM queries inside loops (N+1) | `ProductRepository.list_by_skus` / `InventoryRepository.list_for_skus` load once, then iterate in memory |
| Memory Management | Large allocations inside loops | `stream_rows` / `bounded_map` yield bounded slices |
| Concurrency Analysis | Shared mutable state without locks | `StockLedger` and `LockedCounter` take `threading.Lock` / `RLock` on every mutation |

## Performance → Dependency Analysis

| Gate | What Testable measures | How this repo passes |
|---|---|---|
| Bundle Size Analysis | Unused imports | No dead imports; pinned `requirements.txt` |
| Build Performance | CI duration | `.github/workflows/ci.yml` |
| Dependency Graph Analysis | Circular imports | Layered package (`api` → `services` → `repositories` → `models`) |

## Security → IaC Security

Checkov / tfsec / kics scan `infra/terraform/main.tf`.

| Gate | Pass condition in this repo |
|---|---|
| CIS Benchmark | KMS rotation, VPC flow logs, encrypted logs, RDS backups, IAM DB auth |
| Open Firewall Rules | `0.0.0.0/0` only on TCP 443; app/DB SGs are SG-to-SG only (no SSH/RDP) |
| Public Storage Access | S3 `block_public_* = true`, BucketOwnerEnforced, no public ACL |
| Unencrypted Storage | S3 SSE-KMS, RDS `storage_encrypted`, EBS `encrypted` |

## Security → SOC 2 Compliance

| Gate | Evidence |
|---|---|
| Access Control | Hashed API key compare (`hmac.compare_digest`), empty default key, 401 on missing header |
| Change Management Testing | `CODEOWNERS`, pull request template, Dependabot, GitHub Actions |

## Security → Secret & Credential Scanning

Gitleaks / detect-secrets / TruffleHog.

| Control | Evidence |
|---|---|
| No hardcoded secrets | API key from `ORDERFLOW_API_KEY` only |
| `.env` ignored | `.gitignore` + `.env.example` with empty value |
| Pre-commit | `.pre-commit-config.yaml`, `.gitleaks.toml`, `.secrets.baseline` |

## Compliance → FERPA/COPPA → PII in Log Statements

`orderflow.utils.logging.info` refuses field names `email`, `ssn`, `password`, `pan`, `dob`, `student_id`, `full_name`.
