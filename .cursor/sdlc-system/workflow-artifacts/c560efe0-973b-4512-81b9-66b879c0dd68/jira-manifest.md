# Jira Manifest (Dry Run)

**Workflow ID:** `c560efe0-973b-4512-81b9-66b879c0dd68`  
**Generated:** `2026-08-31T07:00:42.856Z`  
**Mode:** Manifest only (`projectContext.jira.enabled: false`)  
**Project key:** `TBD`  
**SDD:** `docs/sdlc/c560efe0-973b-4512-81b9-66b879c0dd68/containerized-web-app-cicd-pipeline.md`  
**RDD:** `docs/sdlc/c560efe0-973b-4512-81b9-66b879c0dd68/containerized-web-app-cicd-pipeline-requirements.md`  
**Selected scope:** Option 1 - complete requested portfolio baseline  
**Cleanup:** Disabled

No Jira API calls were made. The placeholder keys below are local planning identifiers only. They must not be used as Git branch names or represented as real Jira issues.

## Labels

- `sdlc-workflow`
- `workflowId:c560efe0-973b-4512-81b9-66b879c0dd68`

## Epic

### PENDING-EPIC - Automated CI/CD Pipeline for a Containerized Web Application

Create a complete, beginner-to-intermediate DevOps portfolio project consisting of a stateless Flask application, automated tests, a non-root production container, GitHub Actions CI/CD, and an idempotent single-host Ubuntu EC2 deployment path. Keep all locally verified behavior reproducible and distinguish it from Docker Hub and AWS operations that require the owner's external credentials and infrastructure.

**SDD reference:** Sections 1-10  
**Requirements:** FR-1-FR-16; NFR-1-NFR-13

## Stories and tasks

### PENDING-STORY-1 - Flask web experience - implement application behavior

Build the small application factory, requested routes, responsive presentation, environment-driven version behavior, and isolated route tests.

**SDD reference:** Sections 2-4 and 9  
**Requirements:** FR-1-FR-5, FR-8; NFR-8, NFR-10-NFR-12

Acceptance criteria:

- [ ] `/`, `/about`, and `/health` return the specified successful responses.
- [ ] The home page displays `CI/CD Deployment Successful` and the effective `APP_VERSION`.
- [ ] Gunicorn and pytest instantiate the same application factory.
- [ ] Tests are deterministic and make no external calls.

#### PENDING-TASK-1 - Implement the Flask factory and HTTP routes

Create `app.py` with environment-backed version configuration, HTML routes, health JSON, and a Gunicorn-compatible factory target.

**Traceability:** FR-1, FR-3-FR-5; NFR-8, NFR-11-NFR-12

#### PENDING-TASK-2 - Build the responsive Jinja presentation layer

Create the shared layout, home and About templates, navigation, and stylesheet with the required deployment-success and version content.

**Traceability:** FR-1-FR-2, FR-15; NFR-8

#### PENDING-TASK-3 - Pin Python dependencies and add isolated route tests

Create runtime/development requirement files and pytest coverage for all routes, health semantics, status codes, default version, and overridden version.

**Traceability:** FR-5, FR-8; NFR-9-NFR-11

### PENDING-STORY-2 - Containerized local runtime - package and operate consistently

Provide a production-oriented image and a simple Compose workflow using the canonical internal port 5000.

**SDD reference:** Sections 2-3 and 9  
**Requirements:** FR-5-FR-7; NFR-1-NFR-2, NFR-9, NFR-11-NFR-12

Acceptance criteria:

- [ ] The image runs Gunicorn as a non-root user and declares port 5000 plus a health check.
- [ ] Build context excludes irrelevant and sensitive local artifacts.
- [ ] `docker compose up -d --build` exposes the application at `http://localhost:5000`.

#### PENDING-TASK-4 - Create the secure production Docker image

Add a cache-efficient Python 3.12 Dockerfile with pinned dependencies, an unprivileged runtime user, Gunicorn factory command, and standard-library health probe.

**Traceability:** FR-5-FR-6; NFR-1-NFR-2, NFR-9, NFR-11-NFR-12

#### PENDING-TASK-5 - Add Docker context hygiene and Compose runtime

Create `.dockerignore` and `docker-compose.yml` with `5000:5000`, `APP_VERSION`, build instructions, and visible container health.

**Traceability:** FR-7, FR-14; NFR-2, NFR-9, NFR-12

### PENDING-STORY-3 - Continuous integration - validate every delivery change

Automate application tests, image construction, live health probing, safe diagnostics, and guaranteed cleanup for pushes and pull requests to `main`.

**SDD reference:** Sections 2-3, 6, and 9  
**Requirements:** FR-9, FR-14; NFR-2, NFR-4, NFR-7, NFR-13

Acceptance criteria:

- [ ] CI triggers on pushes and pull requests to `main` with least-privilege permissions.
- [ ] Any test, image-build, startup, or health-probe failure fails the job.
- [ ] Temporary containers are removed even after failure and diagnostics expose no secrets.

#### PENDING-TASK-6 - Implement the GitHub Actions CI workflow

Create `.github/workflows/ci.yml` to check out source, configure Python 3.12, install dependencies, run pytest, build a test image, run it, and probe `/health` with bounded retries.

**Traceability:** FR-9; NFR-2, NFR-4, NFR-7

#### PENDING-TASK-7 - Add CI diagnostics, cleanup, and contract checks

Ensure failed container probes print safe status/log context, cleanup always runs, and triggers, permissions, ports, and commands match the SDD.

**Traceability:** FR-9, FR-14; NFR-2, NFR-4, NFR-7, NFR-12-NFR-13

### PENDING-STORY-4 - Continuous delivery and EC2 deployment - publish and release traceably

Publish the exact successful main-branch commit to Docker Hub under immutable SHA and mutable `latest` tags, then deploy the SHA image to one Ubuntu EC2 host with bounded health verification and best-effort rollback.

**SDD reference:** Sections 2-4, 6, 8, and 9  
**Requirements:** FR-10-FR-14; NFR-2-NFR-7, NFR-12-NFR-13

Acceptance criteria:

- [ ] CD runs only for a successful push-based CI completion on `main` and checks out its exact head SHA.
- [ ] One build is tagged with both the full commit SHA and `latest`; deployment uses the SHA tag.
- [ ] SSH deployment uses only the five named GitHub Secrets and keeps host verification enabled.
- [ ] Deployment is idempotent, maps only `80:5000`, verifies health, and attempts rollback when a prior local image exists.

#### PENDING-TASK-8 - Implement the CI-gated image publication workflow

Create `.github/workflows/cd.yml` with strict `workflow_run` filters, exact-SHA checkout, minimal permissions, Docker Hub authentication, and dual tags from one build.

**Traceability:** FR-10, FR-14; NFR-2, NFR-4, NFR-6-NFR-7

#### PENDING-TASK-9 - Implement idempotent EC2 deployment and rollback

Create executable `scripts/deploy.sh` with strict Bash handling, input validation, pull/replace behavior, previous-image capture, `80:5000`, bounded state/HTTP health checks, sanitized diagnostics, rollback, and first-deployment failure reporting.

**Traceability:** FR-11, FR-13; NFR-3, NFR-5, NFR-7, NFR-12

#### PENDING-TASK-10 - Wire secure SSH deployment into CD

Transfer and invoke the deployment script using `EC2_HOST`, `EC2_USERNAME`, and `EC2_SSH_KEY`, preserve host-key checking, pass the immutable image reference/version, and propagate connection, deployment, and health failures.

**Traceability:** FR-12, FR-14; NFR-2-NFR-4, NFR-7, NFR-13

### PENDING-STORY-5 - Portfolio documentation and final verification - make delivery reproducible and truthful

Document the architecture, decisions, local and external operating procedures, security boundaries, troubleshooting, interview preparation, and evidence limits for a beginner-to-intermediate audience.

**SDD reference:** Sections 1, 3, 7-10  
**Requirements:** FR-14-FR-16; NFR-2-NFR-3, NFR-8-NFR-9, NFR-13

Acceptance criteria:

- [ ] README covers every topic in the SDD acceptance checklist, including at least 20 project-specific interview Q&As and 3-4 truthful resume bullets.
- [ ] Commands and port mappings are reproducible and consistent across code, Docker, workflows, deployment, and documentation.
- [ ] No credential, private key, unsupported external-success claim, duplicate path, dead code, or out-of-scope tooling is present.

#### PENDING-TASK-11 - Author the complete portfolio and operations guide

Create `README.md` with the Mermaid architecture, technology rationale, local/test/Docker/Compose usage, CI/CD explanation, Docker Hub and beginner Ubuntu EC2 setup, security groups, secret provenance, deployment/rollback, troubleshooting, interview Q&A, and resume bullets.

**Traceability:** FR-15-FR-16; NFR-3, NFR-8-NFR-9, NFR-13

#### PENDING-TASK-12 - Perform cross-layer acceptance and security verification

Run the selected Option 1 local verification, review workflow and shell contracts, check canonical ports and secret handling, and explicitly record which Docker Hub/AWS operations remain externally unverified.

**Traceability:** FR-1-FR-16; NFR-1-NFR-13

## Placeholder hierarchy

| Type | Key | Parent |
|---|---|---|
| Epic | `PENDING-EPIC` | - |
| Story | `PENDING-STORY-1` | `PENDING-EPIC` |
| Story | `PENDING-STORY-2` | `PENDING-EPIC` |
| Story | `PENDING-STORY-3` | `PENDING-EPIC` |
| Story | `PENDING-STORY-4` | `PENDING-EPIC` |
| Story | `PENDING-STORY-5` | `PENDING-EPIC` |
| Task | `PENDING-TASK-1` | `PENDING-STORY-1` |
| Task | `PENDING-TASK-2` | `PENDING-STORY-1` |
| Task | `PENDING-TASK-3` | `PENDING-STORY-1` |
| Task | `PENDING-TASK-4` | `PENDING-STORY-2` |
| Task | `PENDING-TASK-5` | `PENDING-STORY-2` |
| Task | `PENDING-TASK-6` | `PENDING-STORY-3` |
| Task | `PENDING-TASK-7` | `PENDING-STORY-3` |
| Task | `PENDING-TASK-8` | `PENDING-STORY-4` |
| Task | `PENDING-TASK-9` | `PENDING-STORY-4` |
| Task | `PENDING-TASK-10` | `PENDING-STORY-4` |
| Task | `PENDING-TASK-11` | `PENDING-STORY-5` |
| Task | `PENDING-TASK-12` | `PENDING-STORY-5` |

No subtasks are proposed for the approved Option 1 scope.
