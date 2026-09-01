# Requirements Discovery Document

**Artifact slug:** `containerized-web-app-cicd-pipeline` (paired SDD: `containerized-web-app-cicd-pipeline.md`)  
**Workflow ID:** `c560efe0-973b-4512-81b9-66b879c0dd68`  
**Date:** `2026-08-31`  
**Status:** READY_FOR_SDD  
**Work type:** `feature`

## 1. Business objective

Create a complete, beginner-to-intermediate DevOps portfolio project for a fresher pursuing DevOps or Cloud Engineer roles: a professional Flask web application whose tests, container build, image publication, and single-host AWS EC2 deployment are automated through GitHub Actions. The finished repository must be reproducible from a fresh clone, understandable enough for the owner to explain in an interview, locally verifiable without cloud credentials, and honest about externally unverified Docker Hub and AWS deployment steps.

## 2. Functional requirements

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| FR-1 | Provide a Flask application with a home page, an About page, and a `GET /health` endpoint using an application factory shared by tests and Gunicorn. | Must | PRD; `coding-standards.mdc` |
| FR-2 | The home experience must use a clean, modern HTML/CSS interface and display both `CI/CD Deployment Successful` and the effective application version. | Must | PRD |
| FR-3 | Read the application version from `APP_VERSION`, defaulting to `1.0.0` when the variable is absent. | Must | PRD |
| FR-4 | Return HTTP 200 and JSON containing `{"status":"healthy"}` from `GET /health`. | Must | PRD; `business-flows.mdc` |
| FR-5 | Serve the application with Gunicorn on container port 5000; the delivered run path must not depend on Flask's development server. | Must | PRD; `architecture.mdc` |
| FR-6 | Package the application with a production-friendly Dockerfile based on a small official Python image, install pinned dependencies with cache-friendly layers, run as a non-root user, expose port 5000, and define a Docker health check. | Must | PRD; `coding-standards.mdc` |
| FR-7 | Provide `.dockerignore` and `docker-compose.yml` so `docker compose up -d` starts the application and makes it available at `http://localhost:5000`. | Must | PRD; `deployment.mdc` |
| FR-8 | Provide pytest coverage proving the home page and health endpoint return HTTP 200, the health response reports `healthy`, and the application version is rendered; `pytest` must run the full suite without external services. | Must | PRD; `coding-standards.mdc` |
| FR-9 | Provide `.github/workflows/ci.yml`, triggered by pushes and pull requests to `main`, that checks out the repository, configures Python, installs dependencies, runs pytest, builds a Docker image, starts a test container, probes `/health`, and cleans up the container; any failed stage must fail CI. | Must | PRD; `deployment.mdc` |
| FR-10 | Provide `.github/workflows/cd.yml` that, after successful validation on the main delivery path, authenticates to Docker Hub through GitHub Secrets, builds the image, and publishes both `DOCKERHUB_USERNAME/devops-web-app:latest` and a commit-SHA tag. | Must | PRD; `architecture.mdc` |
| FR-11 | Provide an executable, idempotent `scripts/deploy.sh` for Ubuntu EC2 that pulls the requested image, captures the previous image for rollback, replaces the existing application container, maps host port 80 to container port 5000, checks container state and `/health`, and emits useful non-secret diagnostics. | Must | PRD; `deployment.mdc`; `coding-standards.mdc` |
| FR-12 | Extend CD so image publication is followed by SSH deployment to EC2 using `EC2_HOST`, `EC2_USERNAME`, and `EC2_SSH_KEY`; execute the deployment script, verify health, and fail the workflow on connection, deployment, or health-check failure. | Must | PRD |
| FR-13 | If the newly started container fails its post-deployment health check and a previous local image exists, automatically replace it with a container from that previous image and report rollback outcome; clearly report when no previous image is available on first deployment. | Must | PRD; `deployment.mdc` |
| FR-14 | Keep Docker Hub and EC2 credentials exclusively in GitHub Secrets named `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `EC2_HOST`, `EC2_USERNAME`, and `EC2_SSH_KEY`; no workflow, script, example, or documentation may contain real credentials. | Must | PRD; `project.mdc` |
| FR-15 | Deliver a professional README with the required overview, Mermaid architecture, technology rationale, local/Docker/test instructions, CI and CD explanations, Docker Hub and beginner-friendly Ubuntu EC2 setup, security-group guidance, secret provenance, deployment and rollback flow, troubleshooting, at least 20 project-specific interview questions with short answers, and 3–4 truthful resume bullets. | Must | PRD |
| FR-16 | Deliver the requested simple repository structure, plus only genuinely necessary supporting files, so a user can clone it, install or build dependencies, run tests, run the container locally, and follow the deployment documentation without hidden repository-local prerequisites. | Must | PRD |

## 3. Non-functional requirements

| ID | Category | Requirement | Verification metric |
|----|----------|-------------|---------------------|
| NFR-1 | Security | The application container must run as a non-root user and expose only its required internal port. | Image inspection shows a non-root runtime user and only port 5000 declared. |
| NFR-2 | Security | Secrets and private keys must not be hard-coded, committed, printed, or embedded in image layers; GitHub Actions must use least-privilege permissions. | Secret scan is clean; workflow permissions are explicitly minimal; logs do not echo secret values. |
| NFR-3 | Network security | Production documentation and deployment must expose HTTP 80 publicly, restrict SSH 22 to the administrator's IP, and never publish container port 5000 directly from EC2. | README security-group rules and deploy command agree with the port model. |
| NFR-4 | Reliability | CI must stop on any failed test, image build, container startup, or health probe and must clean up its test container. | A non-zero command fails the job; cleanup runs even after probe failure. |
| NFR-5 | Reliability | Deployment must be safe to repeat, perform bounded health verification, and attempt a documented previous-image rollback after a failed new release. | Re-running the script does not fail because the named container exists; failure path is testable with a bad image or health response. |
| NFR-6 | Traceability | Each published build must have an immutable commit-SHA image tag in addition to `latest`. | Docker Hub publication steps produce both tags from the same build. |
| NFR-7 | Observability | Container, CI, and deployment failures must emit concise diagnostics sufficient to identify the failed stage without exposing secrets. | GitHub Actions and script output identify test/build/pull/start/health/rollback outcomes. |
| NFR-8 | Maintainability | Python, Bash, workflow, and documentation content must remain small, readable, and beginner-oriented, with comments only where they clarify non-obvious concepts. | Review finds no dead code, duplicate deployment paths, obsolete configuration, or unnecessary dependencies. |
| NFR-9 | Reproducibility | Dependency versions must be pinned where practical, build inputs excluded appropriately, and commands documented so a fresh clone can reproduce tests and the local container. | Fresh-environment `pytest`, Docker build, and Compose startup follow documented commands. |
| NFR-10 | Test isolation | Unit tests must be deterministic and must not call Docker Hub, GitHub, AWS, or any other external service. | `pytest` passes without network access or external credentials. |
| NFR-11 | Compatibility | The implementation must target Python 3.12, Docker/Compose on Linux-compatible hosts, GitHub Actions, and Ubuntu EC2. | Runtime and workflow configuration use the MDC-defined versions and platforms. |
| NFR-12 | Operability | The application and health-check paths must consistently use internal port 5000 locally/in-container and host port 80 only for EC2 production. | Compose, Dockerfile, CI, deploy script, and README have no conflicting port mappings. |
| NFR-13 | Integrity | Documentation and resume claims must distinguish locally verified behavior from Docker Hub/AWS steps that require real credentials and infrastructure. | README and final verification contain no unsupported deployment-success claim. |

## 3b. Technical baseline

Not applicable to this `feature` work type. The workspace is an empty application baseline containing only live SDLC project-context files and workflow state; the requested application and delivery pipeline are new capabilities rather than a migration or replacement. No superseded application artifacts are currently identified for deletion.

## 4. Repositories

> Repository policy is sourced exclusively from `.cursor/project-context/project.mdc`.

### Involved

| Repo | Role | Notes |
|------|------|-------|
| `.` (`D:/DEVOPS-PORTFOLIO/01-CICD-WEB-APP`) | modifiable; primary; local workspace | The physical workspace currently contains `.cursor/project-context/` and workflow state only. No application, test, Docker, workflow, script, README, Git metadata, or remote exists yet. Planned stack and paths are defined by the live MDC files. |

### Modifiable

- `.` — all requested application, test, container, CI/CD, deployment-script, and README artifacts may be created here in later phases.

### Read-only

- None.

### Reconnaissance summary

- Current behavior: there is no runnable application or pipeline to exercise.
- Planned HTTP/business layer: `app.py`, `templates/`, and `static/`.
- Planned tests: `tests/`, using pytest without external services.
- Planned infrastructure: `Dockerfile`, `docker-compose.yml`, `.github/workflows/`, and `scripts/deploy.sh`.
- Planned integrations: GitHub Actions, Docker Hub, and one Ubuntu AWS EC2 host.
- Authentication: no application authentication; CI/CD credentials are injected through GitHub Secrets.
- Local tooling limitation observed during discovery: `git` is not installed or available on `PATH`; Git operations and remote identity could not be inspected.

## 5. Constraints

- Do not introduce Kubernetes, Terraform, ArgoCD, or unrelated advanced tooling.
- Use Python 3.12, Flask, Gunicorn, pytest, Docker, Docker Compose, GitHub Actions, Docker Hub, Bash, and a single Ubuntu AWS EC2 host as defined by the PRD and MDC.
- Keep the project understandable for beginner-to-intermediate DevOps learners; avoid unnecessary dependencies and abstractions.
- Never commit, hard-code, or log credentials, tokens, private keys, or fake production secrets.
- Do not claim Docker Hub publication or AWS EC2 deployment success unless it has been exercised against real external accounts and infrastructure.
- Preserve the monolithic, stateless architecture and environment-variable configuration boundaries described in `architecture.mdc`.
- Bash must use strict error handling, quote variable expansions, and keep deployment idempotent.
- Tests must run with `pytest` and remain independent of external services.
- The production network model is public port 80, administrator-IP-restricted port 22, and non-public container port 5000.
- Delivery is documentation-and-code complete without Jira; `project.mdc` explicitly disables Jira.

## 6. External dependencies

| System | Purpose | Integration style | Owner/team |
|--------|---------|-------------------|------------|
| Python package index | Supply pinned Flask, Gunicorn, pytest, and supporting packages | `pip` package download during setup/build | Python ecosystem / package maintainers |
| Docker Engine and Compose | Build, health-check, and run the application locally and on EC2 | Docker CLI, Dockerfile, Compose | User locally; EC2 operator in production |
| GitHub and GitHub Actions | Source hosting and automated CI/CD execution | Git push/events and workflow YAML | Repository owner |
| Docker Hub | Store `latest` and commit-SHA application images | Registry login, push, and pull | Repository owner / Docker Hub account |
| AWS EC2 | Host the production Docker container on Ubuntu | SSH and host Docker daemon | Repository owner / AWS account |
| GitHub Secrets | Inject Docker Hub and EC2 credentials into CD | Encrypted repository secrets | Repository administrator |

## 7. Assumptions

1. **A-1:** The later implementation phase may create all application and delivery files inside the sole modifiable local workspace (`.`).
2. **A-2:** `main` is the intended default branch even though the empty workspace currently has no Git repository or remote.
3. **A-3:** Docker Hub repository `devops-web-app` will be created or be creatable by the user identified by `DOCKERHUB_USERNAME`.
4. **A-4:** The target EC2 host is Ubuntu, has outbound internet access, and will have Docker plus any deployment prerequisites installed using README instructions.
5. **A-5:** The EC2 user can run Docker commands and bind host port 80, whether through group membership or documented privilege setup.
6. **A-6:** A single named application container is acceptable; brief restart downtime is allowed by the MDC's single-host rolling-replacement strategy.
7. **A-7:** CD will deploy only after CI-equivalent validation succeeds and the image is published successfully; exact workflow dependency/event mechanics are deferred to the SDD.
8. **A-8:** External credentials and hosts will be configured by the user after repository delivery and will not be requested or persisted in this workflow.
9. **A-9:** A health response that validates process readiness is sufficient because the application has no database or other runtime dependency.

## 8. Risks

| ID | Risk | Impact | Likelihood | Mitigation |
|----|------|--------|------------|------------|
| R-1 | Docker Hub and AWS credentials/infrastructure are unavailable in the local environment. | Publication and real EC2 deployment cannot be proven end to end during local delivery. | High | Fully validate unit tests, image build, container health, workflow syntax, and deployment logic locally where possible; clearly document external setup and unverified boundaries. |
| R-2 | Reusing `latest` can make release identity or rollback ambiguous. | The host could pull an unexpected mutable image or lose a clear rollback target. | Medium | Publish a commit-SHA tag, log the deployed tag, capture the pre-deployment local image ID before pulling/replacing, and document limitations. |
| R-3 | A failed first deployment has no prior image. | Automatic rollback is impossible and the service remains unavailable. | Medium | Detect this case, fail clearly, retain diagnostics, and document manual recovery. |
| R-4 | Replacing one container on one EC2 host creates a restart window. | Brief production unavailability during deploy or rollback. | High | State this limitation plainly, minimize replacement time, and defer zero-downtime/multi-host approaches as out of scope. |
| R-5 | SSH key handling or verbose shell output could expose sensitive material. | Credential compromise. | Low | Use GitHub Secrets, avoid shell tracing and secret interpolation in logs, use temporary key handling with restrictive permissions, and apply least-privilege workflow permissions. |
| R-6 | Inconsistent ports or health URLs across Dockerfile, Compose, CI, EC2, and README could make a correct app appear broken. | Local or production startup and probes fail. | Medium | Treat the MDC port model as canonical and cross-check all files during QA. |
| R-7 | The local environment lacks Git, and repository/remote identity is unknown. | Branching, commit, push, CI, and PR phases may be blocked later. | High | Install/configure Git and initialize or connect the repository before Git-dependent delivery phases; do not invent a remote URL. |
| R-8 | Third-party GitHub Actions or floating action versions can create supply-chain risk. | CI/CD behavior could change unexpectedly or execute compromised code. | Medium | Prefer official actions, pin stable versions or immutable SHAs where practical, and use minimal job permissions. |

## 9. Open questions

These do not prevent SDD creation; documented assumptions provide the default design scope.

1. What GitHub repository URL will be used, and will the empty workspace be initialized with `main` as its default branch?
2. Which Docker Hub namespace will own `devops-web-app`, and is the repository public or private?
3. What EC2 hostname, Ubuntu username, AWS region, instance architecture, and administrator source IP will be used?
4. Should CD be triggered directly by a successful push workflow or by completion of a separately defined CI workflow? Default: deploy only after the main-branch commit has passed equivalent CI gates.
5. Should production deploy the immutable commit-SHA tag or `latest`? Default: deploy the SHA tag for traceability while also publishing `latest` as requested.
6. Is SSH host-key pinning information available? Default: document secure known-host configuration and avoid embedding host keys or disabling verification silently.

## 10. Appendix

### Acceptance criteria summary

- `pytest` passes all required route, health, and version tests without external services.
- The Docker image builds, runs as non-root under Gunicorn, and reports healthy on port 5000.
- `docker compose up -d` exposes the application at `http://localhost:5000`.
- CI covers tests, image build, live-container health probing, and cleanup for pushes and pull requests to `main`.
- CD publishes `latest` and commit-SHA tags without hard-coded secrets, then performs a fail-fast SSH deployment with health verification and simple previous-image rollback.
- EC2 exposes only application port 80 publicly, keeps container port 5000 private, and restricts SSH to the administrator's IP.
- README content is complete, beginner-friendly, interview-ready, and truthful about external verification.

### Glossary

- **CI:** Automated validation of each change through tests, image build, and smoke checks.
- **CD:** Automated image publication and deployment after validation.
- **Immutable tag:** A Docker image tag derived from a specific Git commit SHA.
- **Health check:** A probe of `GET /health` used to determine whether the application process can serve requests.
- **Rollback:** Replacing a failed new container with one started from the previously captured local image.

### Reference files reviewed

- Supplied PRD: `Automated CI/CD Pipeline for a Containerized Web Application`
- `.cursor/project-context/README.md`
- `.cursor/project-context/project.mdc`
- `.cursor/project-context/architecture.mdc`
- `.cursor/project-context/coding-standards.mdc`
- `.cursor/project-context/deployment.mdc`
- `.cursor/project-context/business-flows.mdc`
- `.cursor/sdlc-system/state/c560efe0-973b-4512-81b9-66b879c0dd68.json`

### Out of scope

- Kubernetes, Terraform, ArgoCD, managed container platforms, load balancers, autoscaling, multi-host orchestration, and zero-downtime deployment.
- Application authentication, databases, queues, background workers, or business-domain APIs beyond the requested pages and health endpoint.
- Creation or storage of real GitHub, Docker Hub, AWS, or SSH credentials.
- Claiming live Docker Hub publication or AWS deployment without access to and verification against the user's real services.
