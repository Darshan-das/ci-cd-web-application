# Implementation Plan

**Workflow ID:** `c560efe0-973b-4512-81b9-66b879c0dd68`  
**Epic:** `PENDING-EPIC` (Jira dry-run placeholder)  
**SDD:** `docs/sdlc/c560efe0-973b-4512-81b9-66b879c0dd68/containerized-web-app-cicd-pipeline.md`  
**Plan version:** 1.0  
**Status:** PENDING_APPROVAL  
**Selected scope:** Option 1 - complete requested portfolio baseline  
**Cleanup:** Disabled

## Overview

Implement the greenfield portfolio project as one ordered delivery path in the sole modifiable repository, `.`. Begin with the Flask application, pinned dependencies, presentation, and isolated tests; establish the non-root container and Compose runtime next; then automate the same verified contracts in CI before adding image publication and EC2 deployment. Complete the beginner-facing documentation after the operational contracts are stable, and finish with cross-layer acceptance and security verification.

The critical path is `phase-1` through `phase-6`. Docker Hub publication and AWS EC2 deployment require external credentials and infrastructure, so Option 1 plans their code and static/local contract validation but does not claim a successful external run. No cleanup phase is included because cleanup is disabled and the SDD identifies no superseded application artifacts; remove-on-touch hygiene still applies if implementation replaces anything it creates.

### FR/NFR coverage

| FR/NFR | Phases |
|---|---|
| FR-1-FR-4 | `phase-1`, `phase-6` |
| FR-5 | `phase-1`, `phase-2`, `phase-6` |
| FR-6-FR-7 | `phase-2`, `phase-6` |
| FR-8 | `phase-1`, `phase-6` |
| FR-9 | `phase-3`, `phase-6` |
| FR-10 | `phase-4`, `phase-6` |
| FR-11-FR-13 | `phase-4`, `phase-6` |
| FR-14 | `phase-2`, `phase-3`, `phase-4`, `phase-5`, `phase-6` |
| FR-15-FR-16 | `phase-5`, `phase-6` |
| NFR-1 | `phase-2`, `phase-6` |
| NFR-2 | `phase-2`, `phase-3`, `phase-4`, `phase-5`, `phase-6` |
| NFR-3 | `phase-4`, `phase-5`, `phase-6` |
| NFR-4 | `phase-3`, `phase-4`, `phase-6` |
| NFR-5 | `phase-4`, `phase-6` |
| NFR-6 | `phase-4`, `phase-6` |
| NFR-7 | `phase-3`, `phase-4`, `phase-6` |
| NFR-8 | `phase-1`, `phase-5`, `phase-6` |
| NFR-9 | `phase-1`, `phase-2`, `phase-5`, `phase-6` |
| NFR-10 | `phase-1`, `phase-6` |
| NFR-11 | `phase-1`, `phase-2`, `phase-3`, `phase-6` |
| NFR-12 | `phase-1`, `phase-2`, `phase-3`, `phase-4`, `phase-5`, `phase-6` |
| NFR-13 | `phase-3`, `phase-4`, `phase-5`, `phase-6` |

## Phase 1 - Flask application and isolated tests

| Field | Value |
|---|---|
| **ID** | `phase-1` |
| **Name** | Flask application and isolated tests |
| **Goals** | Create `app.py` with a shared Flask application factory, environment-backed `APP_VERSION`, `/`, `/about`, and `/health`; create the shared Jinja layout, responsive pages, navigation, stylesheet, exact success message, and visible version; pin compatible Python 3.12 runtime and test dependencies; add deterministic pytest coverage for all routes, health semantics, status codes, default version, and overridden version. |
| **Jira tasks** | `PENDING-TASK-1`, `PENDING-TASK-2`, `PENDING-TASK-3` |
| **Jira stories** | `PENDING-STORY-1` |
| **Repos** | `.` |
| **Depends on** | `[]` |
| **Exit criteria** | `pytest` passes without network access; focused `pytest tests/test_app.py` passes; `/`, `/about`, and `/health` return HTTP 200; `/health` has healthy JSON semantics; the home page renders `CI/CD Deployment Successful`, default version `1.0.0`, and an overridden safe `APP_VERSION`; Gunicorn and tests can target the same factory. |
| **SDD sections** | Sections 1-5, 8, and 9; AD-1 and AD-2 |
| **Estimated complexity** | M |

## Phase 2 - Secure container and local runtime

| Field | Value |
|---|---|
| **ID** | `phase-2` |
| **Name** | Secure container and local runtime |
| **Goals** | Create a cache-efficient Python 3.12 Dockerfile with pinned installs, an unprivileged runtime user, Gunicorn factory command, only port 5000 exposed, and a standard-library health check; create `.dockerignore` and `.gitignore` exclusions that prevent irrelevant or sensitive local inputs; create `docker-compose.yml` with `5000:5000`, `APP_VERSION`, build configuration, and visible health state. |
| **Jira tasks** | `PENDING-TASK-4`, `PENDING-TASK-5` |
| **Jira stories** | `PENDING-STORY-2` |
| **Repos** | `.` |
| **Depends on** | `["phase-1"]` |
| **Exit criteria** | `docker build -t devops-web-app:test .` succeeds; image inspection shows a non-root user, Gunicorn factory command, port 5000, and a health check; a local container reaches healthy and serves the required routes/version; `docker compose config` is valid; `docker compose up -d --build` exposes the service at `http://localhost:5000`, and teardown removes it cleanly. |
| **SDD sections** | Sections 1b-3, 6, 8, and 9; deployment/runtime notes |
| **Estimated complexity** | M |

## Phase 3 - Continuous integration

| Field | Value |
|---|---|
| **ID** | `phase-3` |
| **Name** | Continuous integration |
| **Goals** | Create `.github/workflows/ci.yml` for pushes and pull requests to `main`; use least-privilege permissions and Python 3.12; install pinned dependencies, run pytest, build a test image, start a uniquely named temporary container, and perform a bounded `/health` probe; add stage-specific sanitized diagnostics and unconditional container cleanup while keeping CI free of deployment secrets. |
| **Jira tasks** | `PENDING-TASK-6`, `PENDING-TASK-7` |
| **Jira stories** | `PENDING-STORY-3` |
| **Repos** | `.` |
| **Depends on** | `["phase-2"]` |
| **Exit criteria** | Workflow triggers and `contents: read`-equivalent minimal permissions match the SDD; the substantive CI commands (`pytest`, image build, container start, bounded health probe, cleanup) pass locally where supported; each failed test/build/start/probe path is configured to fail the job; cleanup is guaranteed after probe failure; workflow output does not expose secrets or full environments. |
| **SDD sections** | Sections 2-3, 6, 8, and 9; AD-3 |
| **Estimated complexity** | M |

## Phase 4 - Continuous delivery and EC2 rollback path

| Field | Value |
|---|---|
| **ID** | `phase-4` |
| **Name** | Continuous delivery and EC2 rollback path |
| **Goals** | Create `.github/workflows/cd.yml` with strict successful push-CI-on-`main` `workflow_run` filters, same-repository validation, exact head-SHA checkout, minimal permissions, Docker Hub login through the named secrets, and one build tagged as both `latest` and full SHA; create executable `scripts/deploy.sh` with strict Bash mode, validation before mutation, previous image/version capture, idempotent replacement, `80:5000`, bounded state and healthy-JSON probes, sanitized diagnostics, verified rollback, and explicit first-deployment behavior; securely establish SSH with a temporary restrictive key and enabled host checking, transfer/invoke the script with the immutable image reference, and propagate all failures. |
| **Jira tasks** | `PENDING-TASK-8`, `PENDING-TASK-9`, `PENDING-TASK-10` |
| **Jira stories** | `PENDING-STORY-4` |
| **Repos** | `.` |
| **Depends on** | `["phase-3"]` |
| **Exit criteria** | Static workflow review proves only successful push CI on `main` can release the exact tested SHA; both Docker tags derive from one build and deployment selects the SHA tag; only `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `EC2_HOST`, `EC2_USERNAME`, and `EC2_SSH_KEY` supply credentials; `bash -n scripts/deploy.sh` passes on a Linux-compatible shell; controlled local/manual Docker scenarios validate repeatability, pre-mutation pull failure, `80:5000`, bounded health behavior, prior-image rollback, and no-prior-image reporting where the environment supports them; unavailable Docker Hub/AWS execution is recorded as externally unverified, not passed. |
| **SDD sections** | Sections 2-6, 8, and 9; AD-3 through AD-7 |
| **Estimated complexity** | L |

## Phase 5 - Portfolio and operations documentation

| Field | Value |
|---|---|
| **ID** | `phase-5` |
| **Name** | Portfolio and operations documentation |
| **Goals** | Create `README.md` with the system overview, Mermaid architecture, technology rationale, repository structure, Python/test/Docker/Compose instructions, CI/CD behavior, Docker Hub setup, beginner-friendly Ubuntu EC2 and Docker setup, security-group rules, provenance of all five secrets, immutable deployment and rollback flow, troubleshooting, limitations, at least 20 project-specific interview questions with short answers, and 3-4 truthful resume bullets; distinguish locally verified results from external Docker Hub/AWS steps and avoid unsupported success claims. |
| **Jira tasks** | `PENDING-TASK-11` |
| **Jira stories** | `PENDING-STORY-5` |
| **Repos** | `.` |
| **Depends on** | `["phase-4"]` |
| **Exit criteria** | README contains every SDD acceptance-checklist topic, at least 20 interview Q&As, and 3-4 truthful resume bullets; documented commands agree with implemented files; local uses host/container `5000:5000`, production uses `80:5000`, and SSH 22 is restricted to the administrator IP; no real/fake credential or unverified external-success claim appears. |
| **SDD sections** | Sections 1, 3, 7-10 |
| **Estimated complexity** | M |

## Phase 6 - Cross-layer acceptance and release readiness

| Field | Value |
|---|---|
| **ID** | `phase-6` |
| **Name** | Cross-layer acceptance and release readiness |
| **Goals** | Run the complete Option 1 local verification matrix across Flask, pytest, image metadata, live container, Compose, CI/CD contracts, Bash parsing and controlled deployment scenarios; cross-check canonical routes, ports, tags, permissions, secret names, health semantics, rollback behavior, documentation, and repository structure; inspect for credentials, private keys, dead code, duplicate deployment paths, development-server production paths, obsolete configuration, dangling references, and out-of-scope tooling; record exact local evidence and explicitly identify Docker Hub/AWS steps that remain externally unverified. |
| **Jira tasks** | `PENDING-TASK-12` |
| **Jira stories** | `PENDING-STORY-5` |
| **Repos** | `.` |
| **Depends on** | `["phase-1", "phase-2", "phase-3", "phase-4", "phase-5"]` |
| **Exit criteria** | `pytest` passes; `docker build -t devops-web-app:test .` and supported container/Compose smoke tests pass; image inspection confirms non-root runtime, port 5000, health check, and Gunicorn; CI/CD and shell contract reviews cover all Option 1 acceptance criteria; secret scan/repository search is clean; every FR-1-FR-16 and NFR-1-NFR-13 has evidence or an explicitly honest external-verification boundary; no excluded tooling or unplanned file is present. |
| **SDD sections** | Sections 1b, 7-10 and the complete acceptance checklist |
| **Estimated complexity** | L |

## Jira coverage

| Jira task | Phase |
|---|---|
| `PENDING-TASK-1` | `phase-1` |
| `PENDING-TASK-2` | `phase-1` |
| `PENDING-TASK-3` | `phase-1` |
| `PENDING-TASK-4` | `phase-2` |
| `PENDING-TASK-5` | `phase-2` |
| `PENDING-TASK-6` | `phase-3` |
| `PENDING-TASK-7` | `phase-3` |
| `PENDING-TASK-8` | `phase-4` |
| `PENDING-TASK-9` | `phase-4` |
| `PENDING-TASK-10` | `phase-4` |
| `PENDING-TASK-11` | `phase-5` |
| `PENDING-TASK-12` | `phase-6` |

All 12 dry-run task placeholders are assigned to exactly one implementation phase. `PENDING-EPIC` is referenced only in the header, and the five story placeholders are used only for story traceability.

## Risk register

| Phase | Risk | Mitigation |
|---|---|---|
| `phase-1` | Dependency pins or factory wiring are incompatible with Python 3.12/Gunicorn. | Select mutually compatible exact versions, use the same `create_app` target in tests and Gunicorn, and pass focused plus full pytest before container work. |
| `phase-2` | User/port/health configuration drift makes the image unsafe or unreachable. | Inspect image metadata and running identity; treat internal 5000, local host 5000, and non-root execution as fixed acceptance contracts. |
| `phase-3` | CI cleanup or `workflow_run` naming assumptions cause leaks or an invalid downstream gate. | Give the CI workflow a stable explicit name, use unique temporary resources, make cleanup unconditional, and cross-review the exact name/event contract before CD. |
| `phase-4` | Missing external resources prevent publication/deployment proof. | Validate locally and statically, never invent credentials or a remote, and label Docker Hub/AWS operations externally unverified. |
| `phase-4` | Rollback metadata, host identity handling, or mutable tags weaken deployment safety. | Capture prior local image ID/version before replacement, deploy the full SHA, keep host checking enabled, avoid secret/environment logging, and verify rollback health before reporting it. |
| `phase-4` | First deployment or occupied port 80 leaves no healthy service. | Detect the absence of a prior image, report it explicitly, retain safe diagnostics, return non-zero, and document manual recovery and the single-host downtime limitation. |
| `phase-5` | Documentation diverges from actual commands or overstates external success. | Author after operational contracts stabilize, copy commands from implemented paths, and maintain a clear locally-verified versus externally-unverified boundary. |
| `phase-6` | Cross-file drift or secret material remains in the repository. | Run the full verification matrix, inspect routes/ports/tags/secret references together, and perform a repository-wide secret and entropy review before handoff. |

## Rollback plan

- Application, presentation, dependency, container, workflow, and documentation changes are greenfield files with no data migration; revert the affected phase's files together if its exit criteria fail.
- Do not advance to a dependent phase while the prior phase is failing. Re-run `pytest` and the relevant Docker/Compose checks after any revert.
- CI and CD remain inert until committed to a GitHub repository with matching events and configured secrets. Disable release behavior by removing/reverting `cd.yml`; do not weaken its gates.
- For an EC2 release failure, `scripts/deploy.sh` removes the failed container and attempts to start the previously captured local image ID with its prior version and `80:5000`; it verifies rollback health and still exits non-zero. If no prior image exists, it reports that rollback is unavailable and leaves the failed release stopped.
- No database or persistent application state exists, so schema or data rollback is not applicable.

## Developer notes

- Use one branch named `containerized-web-app-cicd-pipeline`; do not use dry-run Jira placeholder keys as branch names.
- Execute phases in order. The full test command from live MDC is `pytest`; the focused command is `pytest tests/test_app.py`; the configured image verification command is `docker build -t devops-web-app:test .`.
- Write only in the modifiable repository `.`. Do not add Kubernetes, Terraform, ArgoCD, authentication, persistence, TLS claims, a second deployment mechanism, or infrastructure provisioning.
- Keep the Python, HTML/CSS, Bash, YAML, and documentation small and beginner-readable. Bash must use `set -Eeuo pipefail`, quote expansions, validate inputs before mutation, and avoid tracing secrets.
- Cleanup is disabled and no SDD deletion is planned. Still apply remove-on-touch hygiene: delete any superseded route, file, workflow step, config key, test, or deployment path rather than retaining duplicates.
- Do not claim that Docker Hub publication or AWS EC2 deployment passed unless real authorized external evidence exists. Git availability, remote configuration, credentials, and infrastructure are orchestration/external prerequisites, not values to invent in implementation.
