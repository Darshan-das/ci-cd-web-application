# QA Report

**Workflow ID:** `c560efe0-973b-4512-81b9-66b879c0dd68`  
**Epic:** `PENDING-EPIC` (Jira disabled; manifest only)  
**Branch:** `containerized-web-app-cicd-pipeline` (planned branch; QA validated the physical workspace because Git is unavailable)  
**Commit:** N/A - the workspace is not a Git repository  
**Date:** `2026-08-31T12:22:47.270Z`  
**Selected scope:** Option 1 - complete requested portfolio baseline  
**Cleanup:** Disabled; remove-on-touch entropy policy still applied  
**Retry:** Attempt 1 of 2  
**Verdict:** PASS

## Executive summary

Retry QA independently inspected the current source and confirmed that `scripts/deploy.sh` now compares the Bash command-substituted health response directly with `{"status":"healthy"}`. A disposable Linux-container check passed Bash syntax, accepted the exact body, and rejected `{"status":"heal thy"}`; the malformed response therefore remains a failed health attempt and reaches the existing bounded failure/rollback path. Defect-1 is closed, and FR-13/NFR-5 now pass.

The initial QA baseline for the unchanged application, container, Compose, workflow, documentation, and wider deployment/rollback behavior remains the regression baseline below; the targeted retry did not rerun that complete matrix. Hosted GitHub Actions, Docker Hub publication/pull, self-hosted-runner registration, SSH, and AWS EC2 deployment were not executed because no Git remote, external credentials, or target infrastructure is available. Those are documented external acceptance steps for Option 1 and are not represented as successful external runs.

## Test execution

| Command or check | Exit code | Duration | Result | Evidence |
|---|---:|---:|---|---|
| `pytest` in disposable Python 3.12.12 container, repository mounted read-only | 0 | 0.59s test time | PASS | 12 collected, 12 passed |
| `python -m pytest` in the same isolated environment | 0 | 0.50s test time | PASS | 12 collected, 12 passed |
| `pytest tests/test_app.py` in the same isolated environment | 0 | 0.54s test time | PASS | 12 collected, 12 passed |
| `docker compose config` | 0 | <1s | PASS | One service; `APP_VERSION=1.0.0`; `5000:5000`; exact health check |
| `docker compose up -d --build` | 0 | ~2s | PASS | Image built from `python:3.12.12-slim-bookworm`; service reached healthy |
| Live `GET /`, `GET /about`, and `GET /health` | 0 | <2s | PASS | HTTP 200; success text and `Version 1.0.0`; healthy JSON |
| Live unknown route and `POST /health` | 0 | <1s | PASS | HTTP 404 and 405 respectively |
| Image metadata inspection | 0 | <1s | PASS | `User=app`; only `5000/tcp`; exact health check; Gunicorn factory command |
| `docker compose exec -T web id` and `docker compose top` | 0 | <1s | PASS | UID 100/GID 101; Gunicorn master plus two workers |
| PyYAML parse of `ci.yml` and `cd.yml` | 0 | <1s each | PASS | Both files parsed successfully |
| `bash -n scripts/deploy.sh` in a disposable Linux container (retry) | 0 | 0.55s | PASS | Current script is valid Bash; independent raw-file inspection also found a valid shebang, LF line endings, and no CRLF |
| Exact health-body acceptance assertion in Bash (retry) | 0 | 0.62s | PASS | Exact `{"status":"healthy"}` was accepted by direct equality |
| Malformed health-body rejection assertion in Bash (retry) | 0 | 0.54s | PASS | `{"status":"heal thy"}` was rejected; the assertion exits 0 only on rejection |
| Credential/private-key/token pattern scan | 1 (no matches) | <1s | PASS | No credential-shaped values found in delivered source/config |
| `docker compose down`; post-cleanup `docker compose ps --all` | 0 | ~1s | PASS | QA container and network removed; no Compose containers remain |

The supplied Phase 6 evidence was also reviewed for the controlled offline deployment scenarios: first success, repeat deployment, pull failure before mutation, invalid input, unhealthy release with verified previous-image rollback and final non-zero status, unhealthy first deployment with explicit no-rollback reporting, and exact `80:5000` publication. All were recorded as passed. The retry independently inspected `scripts/deploy.sh` to confirm the exercised behavior and fixed predicate are present. The developer's focused retry claims were corroborated, although the implementation summary does not retain the exact comparison commands or their exit codes; the independent retry evidence above supplies them.

## Requirements traceability

| ID | Priority | Status | Evidence |
|---|---|---|---|
| FR-1 | Must | PASS | `app.py:create_app`; route test parameterization; live `/`, `/about`, `/health` all returned 200; Docker command uses `app:create_app()` |
| FR-2 | Must | PASS | `templates/index.html` contains the exact success text and rendered version; responsive presentation is implemented in `static/css/style.css`; automated and live checks passed |
| FR-3 | Must | PASS | Factory reads `APP_VERSION` with `1.0.0` fallback; tests cover absent, empty, and overridden values |
| FR-4 | Must | PASS | `test_health_returns_exact_healthy_semantics`; live `/health` returned HTTP 200 and `{"status":"healthy"}` |
| FR-5 | Must | PASS | Image command is Gunicorn on `0.0.0.0:5000` with the factory target; live process inspection showed one master and two workers; no production Flask development-server path exists |
| FR-6 | Must | PASS | Docker build passed; exact Python 3.12 slim tag, pinned requirements layer, unprivileged `app` user, only port 5000, and Docker health check verified by inspection |
| FR-7 | Must | PASS | `.dockerignore` excludes non-runtime inputs; Compose config passed; `docker compose up -d --build` made the app healthy at localhost:5000 and teardown passed |
| FR-8 | Must | PASS | Bare pytest, module pytest, and scoped pytest each passed all 12 deterministic tests with no external service calls |
| FR-9 | Must | PASS | `ci.yml` parsed and contains push/PR `main` triggers, Python 3.12 setup, dependency install, pytest, image build, temporary container, bounded exact-health probe, failure diagnostics, and `always()` cleanup; substantive local commands passed |
| FR-10 | Must | PASS | `cd.yml` parsed; release is gated on successful same-repository push CI for `main`, checks out `head_sha`, logs in via Secrets, and one build/push step publishes `latest` plus the full SHA tag; external publication remains unverified |
| FR-11 | Must | PASS | Delivered LF/shebang Bash script passed `bash -n`; static review and controlled offline evidence cover validation, pull-before-mutation, idempotent replacement, `80:5000`, bounded health, and diagnostics. Git mode is an explicit repository-initialization acceptance step, while both documented and workflow paths invoke Bash directly |
| FR-12 | Must | PASS | CD validates the three EC2 inputs, creates restrictive temporary SSH files, keeps strict host checking enabled, streams the exact checked-out script, passes the immutable image/SHA, and propagates SSH/script failure; live EC2 remains unverified |
| FR-13 | Must | PASS | Current `wait_for_healthy_release` uses direct quoted equality with `{"status":"healthy"}` and no body normalization. Independent Bash assertions accepted the exact body and rejected `{"status":"heal thy"}`; a differing body exhausts the bounded check and enters the existing failed-release rollback path. Prior controlled evidence verifies previous-image restoration, rollback health, and a final non-zero release result |
| FR-14 | Must | PASS | Workflow references exactly the five required Secret names; source scan found no credential/key/token value; no `set -x` or environment dump is present |
| FR-15 | Must | PASS | README contains overview, Mermaid architecture, rationale, local/test/Docker/CI/CD/Docker Hub/EC2/security/secrets/deploy/rollback/troubleshooting material, 28 interview Q&As, and four final resume bullets |
| FR-16 | Must | PASS | Every planned runtime/supporting file is present, commands were exercised from the repository root, and no hidden repository-local runtime prerequisite or excluded advanced tool was found |

## NFR validation

| ID | Category | Status | Evidence / notes |
|---|---|---|---|
| NFR-1 | Security | PASS | Image reports `User=app`, running UID 100, and only `5000/tcp` in `ExposedPorts` |
| NFR-2 | Security | PASS | Secret scan clean; workflows declare only `contents: read`; exact five Secret references; no secret echo/environment dump; runtime image excludes local secret files |
| NFR-3 | Network security | PASS | Deploy script publishes only `80:5000`; README allows public 80, administrator-IP `/32` for SSH 22, and explicitly forbids public 5000 |
| NFR-4 | Reliability | PASS | CI steps fail normally on non-zero results, probe is bounded, diagnostics run on failure, and cleanup uses `if: always()`; local substantive test/build/start/probe path passed |
| NFR-5 | Reliability | PASS | Repeatability, bounded attempts, and rollback scenarios remain covered by the initial controlled evidence. The fixed direct comparison now fails closed for a malformed status value, independently closing the exact-health gap without changing the rollback flow |
| NFR-6 | Traceability | PASS | One CD build/push action emits both `latest` and full `workflow_run.head_sha` tags, and deployment selects the SHA reference |
| NFR-7 | Observability | PASS | CI and deployment paths print stage-specific bounded diagnostics without dumping environments or secrets; release and rollback outcomes are explicit |
| NFR-8 | Maintainability | PASS | Small factory/templates/tests/workflows/script; no unnecessary dependency, duplicate deployment path, dead route, commented-out implementation, or obsolete config found |
| NFR-9 | Reproducibility | PASS | Direct dependencies and Python image patch are pinned; `.dockerignore` is scoped; fresh isolated pytest, Docker build, and Compose startup passed using documented commands |
| NFR-10 | Test isolation | PASS | Tests use Flask's local test client only and passed without GitHub, Docker Hub, AWS, or application network dependencies |
| NFR-11 | Compatibility | PASS | Tests ran on Python 3.12.12; image is Debian/Linux Python 3.12; workflows target GitHub Actions; deploy script and guide target Ubuntu |
| NFR-12 | Operability | PASS | App/Docker/CI use internal 5000; Compose uses local `5000:5000`; EC2 script uses only `80:5000`; no conflicting production mapping found |
| NFR-13 | Integrity | PASS | README and implementation evidence repeatedly distinguish local/offline verification from hosted CI, Docker Hub, runner, SSH, and EC2 operations not yet executed |

## SDD edge cases

| Case | Status | Evidence |
|---|---|---|
| `APP_VERSION` absent | PASS | Automated default-version test and live Compose default `1.0.0` |
| Template-sensitive version | PASS | Automated Jinja escaping test rejects raw script markup and finds escaped text |
| Unknown route or POST to GET-only endpoint | PASS | Live 404/405 checks; POST parameterized tests for all three routes |
| Dependency installation or test failure | PASS (contract inspection) | CI has no failure suppression; a non-zero install/test step stops the job |
| Test container never starts or never becomes healthy | PASS (contract inspection) | Bounded 30-second probe, failure diagnostics, and unconditional cleanup |
| Duplicate/re-run CI | PASS (contract inspection) | Run/attempt-specific container name and unconditional removal |
| Repeated deployment of the same image | PASS | Supplied controlled offline repeat scenario; named container capture/remove/recreate logic inspected |
| Invalid or empty deployment arguments | PASS | Supplied invalid-input scenario; validation and usage failure occur before mutation |
| Docker pull or SSH connection failure | PASS | Pull-before-mutation scenario passed; SSH is fail-fast under strict Bash with bounded connection settings |
| Existing named container is stopped | PASS (inspection) | Capture logic uses `docker container inspect` independent of running state and preserves its local image/version |
| Port 80 already occupied | PASS (inspection) | Failed `docker run` enters diagnostics and rollback handling; README documents that the conflict can also prevent rollback |
| New container is running but returns wrong JSON/non-200 | PASS | `curl --fail` rejects non-200, and the current direct body equality rejects `{"status":"heal thy"}`. Independent retry assertions cover exact acceptance and malformed rejection; failed attempts continue through the bounded loop and existing rollback handling |
| Failed new release with previous image | PASS | Controlled offline scenario verified prior image/version restoration, health, and final non-zero release result |
| Failed first release | PASS | Controlled offline scenario verified explicit no-rollback reporting and non-zero result |
| Rollback image exists but rollback health fails | PASS (inspection) | Script reports rollback failure, prints bounded diagnostics, removes the unhealthy rollback container, and exits non-zero |
| Pull-request CI succeeds | PASS (contract inspection) | CD requires `workflow_run.event == 'push'`, `head_branch == 'main'`, success, and same repository |
| Missing or invalid GitHub Secret | PASS (contract inspection) | Explicit identity/input validation plus unsuppressed login/SSH failures; no secret values are printed |
| Private Docker Hub repository | PASS (documented boundary) | Option 1 explicitly supports a public repository; private-host authentication is truthfully documented as not implemented |

## Coverage

Coverage tooling and a numeric threshold are not configured in `coding-standards.mdc`. No line or branch percentage is claimed. The 12-test suite directly exercises all three routes, success text, default/empty/overridden/escaped versions, exact health JSON, About content, and GET-only behavior; Docker and Compose smoke checks exercise the production server path. The principal remaining evidence gap is external integration execution, not uncovered local application behavior.

## Defects

No open defects.

### Defect-1 (Major) - CLOSED - Malformed health JSON could bypass host-side rollback

- **Requirements:** FR-13, NFR-5; SDD edge case "New container is running but JSON is wrong/non-200"
- **Original issue:** The former predicate removed all whitespace from the raw response, allowing `{"status":"heal thy"}` to become `{"status":"healthy"}`.
- **Fix inspected:** `wait_for_healthy_release` now compares the command-substituted response directly with the quoted literal `{"status":"healthy"}` and contains no response-body whitespace normalization.
- **Independent retry evidence:** Current-script `bash -n` exited 0; the exact-body acceptance assertion exited 0; the malformed-body rejection assertion exited 0. The current file has a valid Bash shebang, LF line endings, and no CRLF.
- **Outcome:** Exact healthy output remains accepted after Bash strips the response's trailing newline. Embedded, leading, trailing, or structural body differences remain different and therefore fail closed into the existing bounded failure/rollback flow.

## Regression notes

- The retry source delta was inspected in the current physical workspace: script, SDD, README, and implementation evidence consistently specify direct exact-body comparison with no whitespace normalization.
- Current-script Bash syntax passed independently in a disposable Linux container.
- Focused Bash regression assertions accepted `{"status":"healthy"}` and rejected `{"status":"heal thy"}`.
- The three pytest entry points, production image/runtime, Compose, workflow contracts, and wider offline deployment/rollback matrix passed the initial QA baseline with no flaky or pre-existing failures. They were not rerun for this targeted retry.
- The implementation summary records the developer syntax and focused comparison results but not their exact commands or exit codes; QA supplied independent command/exit-code evidence above.
- Hosted CI cannot provide a check URL until Git and a GitHub remote exist; this is recorded as an external acceptance boundary rather than fabricated regression evidence.

## Entropy / stale assets

| Check | Status | Notes |
|---|---|---|
| Orphaned tests vs deleted code | PASS | Greenfield scope; no SDD deletion list; every test targets a live factory/route |
| FR evidence vs removed endpoints | PASS | All three documented routes exist and passed live checks |
| Stale test references | PASS | Full suite collects and passes all 12 tests |
| Dead/commented-out code in delivered files | PASS | None found in inspected Python, templates, CSS, workflows, Docker/Compose, or Bash |
| Duplicate deployment/runtime path | PASS | One Gunicorn container path, one CI workflow, one CD workflow, and one deployment script |
| Obsolete config or dangling file reference | PASS | Delivered path and command references resolve; no generated caches or temporary harness remains |
| SDD removal list / cleanup selection | PASS | No removals planned; cleanup is false; remove-on-touch fixes and generated-cache cleanup are documented |
| Config-only delivery check | PASS | Application source, presentation, tests, runtime, workflows, script, and documentation are all delivered |

## External acceptance boundary

The following were not run and are not claimed as passing external integrations:

- Hosted GitHub Actions CI or CD and their check URLs.
- Git branch/commit/push/PR behavior or Git mode `100755` for `scripts/deploy.sh`.
- Docker Hub login, dual-tag publication, or target-repository pull.
- Registration and operation of the labeled trusted self-hosted runner.
- SSH connectivity, host identity against an independently trusted fingerprint, real EC2 deployment, public port-80 reachability, or live EC2 rollback.

The repository contains explicit setup and verification steps for each boundary. Before production acceptance, initialize/connect Git, preserve the script executable bit, configure the public Docker Hub repository and five Secrets, register the controlled-egress runner, require the hosted CI check, run CD, verify both tags, and exercise the documented EC2 health and rollback scenarios with sanitized evidence.

## Sign-off

- **QA Agent:** automated, independent physical-workspace validation
- **Ready for impact analysis:** yes
