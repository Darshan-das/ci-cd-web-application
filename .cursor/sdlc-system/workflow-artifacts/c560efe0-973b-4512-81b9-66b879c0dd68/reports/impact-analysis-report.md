# Impact Analysis Report

**Workflow ID:** `c560efe0-973b-4512-81b9-66b879c0dd68`  
**Branch:** `containerized-web-app-cicd-pipeline` (planned branch; not materialized because Git is unavailable)  
**Date:** `2026-08-31T12:49:04Z`  
**Risk Level:** MEDIUM  
**Breaking Change Count:** 0  
**Analysis basis:** Complete greenfield physical workspace plus the implementation summary  
**QA entry gate:** PASS after retry; ready for impact analysis

## Scope and Evidence Basis

The pre-report physical workspace contained 30 delivered files. This analysis independently read the live project MDC files, RDD, SDD, implementation plan, implementation summary, retry QA report, workflow state and manifest, and every delivered application, test, container, workflow, deployment, presentation, and operations file.

A normal base-branch diff could not be produced: the physical workspace has no `.git` directory and neither `git` nor `gh` is installed. There is therefore no commit, executable-mode record, remote, or trustworthy `origin/main...HEAD` comparison. In accordance with the greenfield delivery record, the complete physical workspace and the implementation summary's phase-by-phase file inventory are treated as the change set. This limitation reduces provenance and mode-change assurance but does not prevent component-level impact analysis; no diff or commit evidence is fabricated.

The retry QA report records `PASS`, no open defects, and independent confirmation of the corrected exact health-body predicate. Impact analysis does not repeat QA's FR/NFR verdict or acceptance execution.

## Risk Rationale

The change is not isolated: it creates a public HTTP surface, a runtime configuration contract, a non-root container, CI/CD gates, registry publication, a secret-bearing self-hosted runner path, and single-host EC2 replacement/rollback. Several consumers are coupled to exact names, ports, tags, labels, and health semantics, so LOW would understate the operational blast radius.

The risk is not HIGH or CRITICAL because this is a greenfield baseline with no pre-existing consumers to migrate, no authentication/security contract change to an existing service, no shared-library break, no database or event schema, no destructive migration, and no unversioned replacement of an existing public API. The remaining exposure is known deployment/configuration risk with documented setup and rollback boundaries, which fits MEDIUM.

## Changed Components

| # | Component | Layer | Files | Summary |
|---:|---|---|---|---|
| 1 | Flask HTTP/business surface | HTTP, business | `app.py` | Creates the shared application factory and new `GET /`, `GET /about`, and `GET /health` routes; reads `APP_VERSION` with a `1.0.0` default (`app.py:10-40`). |
| 2 | Presentation | HTTP | `templates/base.html`, `templates/index.html`, `templates/about.html`, `static/css/style.css` | Adds the browser-visible portfolio UI, navigation, deployment status, and escaped version rendering. |
| 3 | Dependency and test contract | Cross-cutting | `requirements.txt`, `requirements-dev.txt`, `pytest.ini`, `tests/test_app.py` | Pins direct Python dependencies and creates deterministic coverage for all routes, version behavior, escaping, JSON health, and method rejection. |
| 4 | Container and local runtime | Infrastructure | `Dockerfile`, `.dockerignore`, `docker-compose.yml` | Creates a Python 3.12/Gunicorn image, switches to unprivileged user `app`, exposes only container port 5000, defines exact health checks, and maps local `5000:5000` (`Dockerfile:22-29`; `docker-compose.yml:7-21`). |
| 5 | Continuous integration | Infrastructure | `.github/workflows/ci.yml` | Adds push/PR validation for `main`, pytest, image build, loopback-only ephemeral container smoke testing, bounded health probing, diagnostics, and unconditional cleanup (`ci.yml:1-12`, `ci.yml:40-113`). |
| 6 | Continuous delivery | Infrastructure | `.github/workflows/cd.yml` | Adds successful same-repository push-CI gating, exact-SHA checkout, public Docker Hub dual-tag publication, and secret-bearing SSH deployment on a labeled controlled-egress self-hosted runner (`cd.yml:1-38`, `cd.yml:70-150`). |
| 7 | EC2 deployment and rollback | Infrastructure | `scripts/deploy.sh` | Adds pull-before-mutation replacement of `devops-web-app`, production `80:5000`, `APP_VERSION`/release-label propagation, bounded exact health validation, prior-image rollback, and first-deploy failure handling. |
| 8 | Operations, repository hygiene, and delivery records | Cross-cutting | `README.md`, `.gitignore`, `.cursor/project-context/**`, `docs/sdlc/**`, workflow artifacts | Defines external prerequisites, canonical contracts, known limitations, traceability, security-group guidance, and the honest local-versus-external verification boundary. |

**Direct impact count:** 8

## Direct Impact

1. **Three new HTTP routes become the complete application contract.** `/` and `/about` are browser-facing HTML; `/health` is a public, unauthenticated, side-effect-free JSON signal. Unknown paths and unsupported methods retain Flask's normal 404/405 behavior.
2. **`APP_VERSION` becomes a cross-layer release identity.** The app defaults absent or empty values to `1.0.0`; Compose supplies the same default; CD supplies the full tested commit SHA; deployment stores it in both the container environment and `devops-web-app.version` label so rollback can restore the visible version.
3. **The production process boundary moves into a non-root container.** Gunicorn binds inside the container on `0.0.0.0:5000`, while runtime user `app` cannot rely on root privileges or writable application directories. Future features that write under `/app` or bind privileged container ports would be incompatible without an explicit design change.
4. **Health becomes a release gate rather than informational telemetry.** Dockerfile and Compose parse the JSON payload; CI requires HTTP 200 and JSON equality; EC2 deployment additionally requires Docker state `running`, Docker health `healthy`, and the command-substituted body to equal `{"status":"healthy"}` exactly (`scripts/deploy.sh:100-140`).
5. **CI becomes the required main delivery validator.** Renaming workflow `CI`, changing its trigger, weakening failure propagation, changing internal port 5000, or changing health semantics would directly affect CD eligibility.
6. **CD introduces a privileged operational trust boundary and release-order dependency.** A successful main push can execute repository code on a self-hosted runner that has Docker, registry credentials, an EC2 private key, and network reachability. The runner must be dedicated to trusted repositories, patched, correctly labeled, and protected through repository/branch administration. CD deploys the successful CI run's exact SHA but does not prove that SHA is still current `main`; out-of-order CI completions or reruns can therefore deploy an older tested commit after a newer one.
7. **Production adopts one fixed Docker/EC2 namespace.** Image repository `DOCKERHUB_USERNAME/devops-web-app`, container name `devops-web-app`, version label `devops-web-app.version`, and host/container mapping `80:5000` are operational interfaces used by workflow, script, diagnostics, documentation, and rollback.
8. **Rollback becomes local-image dependent.** The script preserves the prior container's image ID/version before mutation and keeps a pull failure non-disruptive, but rollback availability depends on that image remaining in the EC2 cache and port 80 remaining usable.

## Downstream Impact

1. **Browser visitors and operators:** receive the new pages over local port 5000 or production port 80. They depend on template rendering and version visibility; production traffic is plain HTTP in this baseline.
2. **Health consumers:** Docker Engine, Compose, CI, the deployment script, and operators depend on `/health`. A semantically equivalent but differently serialized response could still fail the host deployment's intentionally exact body check and initiate rollback.
3. **Contributors and branch protection:** pushes/PRs to `main` now incur pytest, Docker build, and live smoke gates. Repository rules must require the hosted `CI` check for this to become an enforced merge control rather than only a checked-in workflow.
4. **Docker Hub consumers:** the repository publishes public `latest` and full-SHA tags before EC2 input/connectivity and release health are validated. A failed deployment can therefore leave `latest` pointing at a failed candidate rather than the running production release. EC2 intentionally pulls without registry credentials, so changing the repository to private breaks deployment until an approved host-authentication lifecycle is added.
5. **Self-hosted runner operators:** must supply a trusted Linux x64 runner labeled `devops-web-app-deploy`, Docker/Buildx, Git/Bash/OpenSSH tooling, GitHub and Docker Hub egress, and a stable source IP permitted by the EC2 SSH `/32` rule.
6. **EC2 host and public clients:** the host must be Ubuntu/x86-compatible, have Docker and curl, permit the deployment user to use Docker, leave host port 80 available, keep container port 5000 private, and allow outbound public Docker Hub access. The script validates loopback health; security-group, route, DNS, and public reachability remain separate operator checks.
7. **Release and incident operators:** a failed new image keeps CD red even after a healthy rollback, which is desirable visibility. Operators must retain a known-good image/SHA, avoid pruning the last working local image, and have a manual recovery path for first deployment, port conflict, unhealthy prior release, or later post-deployment degradation.

**Downstream impact count:** 7

## Upstream Impact

- **Python/PyPI:** Python 3.12, Flask, Gunicorn, and pytest are required. Direct packages are pinned, but transitive resolution is not fully locked; dependency changes require the route/container matrix to be repeated.
- **Base image and action publishers:** `python:3.12.12-slim-bookworm` is tag-pinned rather than digest-pinned, and GitHub Actions use major-version refs rather than commit SHAs. A future rebuild can therefore consume changed upstream content even at the same application commit.
- **Docker Engine/Buildx:** local, CI, runner, and EC2 flows assume compatible Linux Docker behavior, image health metadata, bridge publishing, and access to the daemon. Docker-group access is effectively host-root privilege and enlarges the runner/EC2 trust boundary.
- **GitHub:** `workflow_run`, repository identity, `main`, exact workflow name `CI`, five repository Secrets, runner labels, Actions availability, and branch protection are external control-plane dependencies not provisioned by this repository.
- **Docker Hub:** the namespace and public `devops-web-app` repository must exist, the token must permit publishing, anonymous EC2 pulls must be allowed, and the runner/host must tolerate registry availability or rate limits.
- **AWS/network/SSH:** EC2 identity, x86-compatible image architecture, DNS/IP stability, admin-controlled `/32` SSH ingress, public HTTP 80, outbound registry access, private-key validity, and OpenSSH host-key behavior are upstream prerequisites. `ssh-keyscan` enables strict matching for the discovered key but does not independently authenticate first contact.

## Potential Breaking Changes

No breaking change is introduced relative to the documented empty baseline.

| ID | Change | Affected consumers | Mitigation |
|---|---|---|---|
| None | No pre-existing API, event, schema, shared-library, deployment, or persisted-data contract was replaced. | None requiring migration or coordinated upgrade. | Establish the new contract-sensitive values below as documented interfaces before onboarding consumers. |

The following are **future contract sensitivities**, not current breaking changes and therefore are not included in `breakingChangeCount`:

- Route paths/methods and the exact `/health` wire body.
- `APP_VERSION`, its `1.0.0` fallback, and the `devops-web-app.version` rollback label.
- Workflow names `CI`/`CD`, branch `main`, successful-push/same-repository predicates, and runner label `devops-web-app-deploy`.
- The five Secret names, Docker Hub namespace/repository, `latest` plus full-SHA tag scheme, and public-repository assumption.
- Container name `devops-web-app`, internal port 5000, local `5000:5000`, production `80:5000`, and loopback production health URL.

## Compatibility Risks

| ID | Risk | Impact | Control / mitigation |
|---|---|---|---|
| C-1 | A future Flask/JSON formatting change preserves semantic JSON but changes bytes. | EC2 deploy health fails and may roll back while Docker/CI JSON parsers still pass. | Treat the exact wire body as a versioned operational contract or deliberately change all health consumers together. |
| C-2 | Future application code assumes root or a writable `/app`. | Container startup/runtime failures under user `app`. | Keep runtime state outside the image layer or add an explicitly owned writable path; retain the non-root gate. |
| C-3 | EC2 architecture differs from the x64 release runner's build output. | Image pull/run can fail even when CI passed. | Keep the documented x86_64 EC2 baseline or explicitly add and validate multi-platform builds. |
| C-4 | Docker Hub repository is private. | EC2 anonymous pull fails before mutation; the existing release remains, but deployment cannot advance. | Preserve the public baseline or obtain approval for a separate least-privilege host registry-auth design. |
| C-5 | `CI`, `main`, runner labels, Secret names, container name, ports, or image path drift independently. | Release skips, queues indefinitely, publishes incorrectly, cannot connect, or cannot health-check/rollback. | Review these as one cross-file interface and update workflow, script, MDC/SDD, tests, and README atomically. |
| C-6 | Git initialization does not preserve `scripts/deploy.sh` mode `100755`. | Direct `./scripts/deploy.sh` use fails, although checked-in CD still works because it invokes remote Bash explicitly. | Set and verify executable mode when Git is initialized and before publish. |

## Deployment Risks

| ID | Risk | Likelihood | Impact | Mitigation / gate |
|---|---|---|---|---|
| D-1 | Hosted GitHub Actions, Docker Hub, self-hosted runner, SSH, and EC2 have not been exercised. | High until external setup | High | Treat the first real pipeline run as an external acceptance gate; require evidence for CI, both tags, public pull, SSH, loopback/public port 80, and rollback before production acceptance. |
| D-2 | The secret-bearing self-hosted runner is unavailable, mislabeled, compromised, or lacks tools/controlled egress. | Medium | High | Use a dedicated patched Linux x64 runner, restrict repository access, verify Docker/Buildx/OpenSSH/Git/Bash, labels, service health, egress IP, and queued-job alerting. Keep deployment concurrency serialized. |
| D-3 | `ssh-keyscan` discovers a key on every ephemeral job without an independently trusted fingerprint. | Low to Medium | High | Verify and pin the expected EC2 host fingerprint through an approved secure configuration mechanism before treating the path as hardened; never disable strict host checking. |
| D-4 | Successful CI runs can complete or be rerun out of order; CD verifies the tested SHA but not that it is still current `main`. Concurrency serializes deployments but does not make them monotonic. | Medium | High | Protect `main` and add a just-before-release freshness/monotonicity gate so an older successful run cannot publish/deploy after a newer accepted release. |
| D-5 | CI and CD rebuild separately; action refs/base image are mutable, and Docker Hub does not enforce SHA-tag immutability. | Medium | Medium to High | Record published digests, prevent/monitor SHA-tag overwrite, consider digest pinning or artifact promotion in a future approved hardening scope, and keep exact-SHA checkout. |
| D-6 | Both registry tags are published before EC2 inputs/connectivity and deployed health are validated. A failed release can make registry `latest` diverge from the running production version. | Medium | Medium to High | Define `latest` as candidate or production explicitly; preferably publish the immutable SHA first and advance the production alias only after successful deployment/public verification. |
| D-7 | Port 80 is occupied or the AWS/network path is misconfigured. | Medium | High | Preflight the host, reserve port 80, enforce SG public 80/admin-controlled SSH 22/no public 5000, and perform a separate external public-path check because deploy verifies loopback only. |
| D-8 | Single-host stop/remove/start produces an interruption; first deployment or pruned/unhealthy prior image has no safe automatic rollback. | Medium | High | Accept the documented restart window, retain the last known-good local image and registry SHA, prohibit unsafe pruning, rehearse manual SHA rollback, and define first-deploy recovery. |
| D-9 | Actions concurrency protects only this workflow group; a manual/direct script invocation can race CD on the same fixed container name and port. | Low to Medium | High | Establish exclusive operating procedure or host-side locking around deployment and rollback; do not run manual and automated replacement concurrently. |
| D-10 | A running container becomes unhealthy after the bounded deployment window. | Medium | Medium | Add external monitoring/alerting and an operator runbook; `unless-stopped` is not continuous unhealthy-container remediation. |
| D-11 | Plain HTTP on public port 80 exposes traffic without TLS. | High for real Internet use | Medium to High | Keep this as the documented portfolio baseline only; add an approved TLS termination design before handling sensitive or production traffic. |

### Deployment order

1. Initialize/connect Git on `main`, set `scripts/deploy.sh` executable mode, push the complete change set, and configure branch protection to require `CI`.
2. Create the **public** Docker Hub `devops-web-app` repository and configure the five exact GitHub Secrets.
3. Provision and harden the labeled controlled-egress Linux x64 self-hosted runner; verify its source IP matches EC2 SSH ingress.
4. Provision Ubuntu x86_64 EC2 with Docker/curl, Docker access for the deployment user, outbound Docker Hub connectivity, SSH 22 limited to the approved `/32`, public HTTP 80, no public 5000, and an unused host port 80.
5. Run hosted CI for the exact commit, confirm it remains the accepted/current `main` release, then allow CD to publish and deploy the immutable SHA tag.
6. Verify container/Docker/loopback health, then separately verify the public port-80 path and displayed `APP_VERSION`; advance or interpret `latest` according to the explicitly chosen registry-alias semantics.
7. Exercise a sanitized failure/rollback scenario while a known-good prior image is retained; record first-deployment recovery separately and ensure manual deployment cannot race CD.

There is no database or event migration and therefore no service/schema deployment ordering requirement. CI must precede CD, publication must precede EC2 pull, and the immutable SHA tag—not `latest`—must be selected for deployment.

## API / Event / Schema / Config Notes

### API

- New unauthenticated, read-only routes: `GET /`, `GET /about`, and `GET /health`.
- `/health` returns HTTP 200 and `application/json`; Flask currently emits `{"status":"healthy"}` plus a trailing newline. Bash command substitution removes the newline before the exact comparison.
- No request DTOs, query contracts, custom error payloads, authentication, or rate limiting are introduced.

### Events and shared libraries

- No event, queue, topic, message payload, internal shared library, or exported package API exists.

### Database/schema

- No database, persistent application state, migration, backfill, PII store, destructive change, or rollback ordering exists.

### Configuration and operational interfaces

- Optional application setting: `APP_VERSION` with default `1.0.0`.
- Required CD Secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `EC2_HOST`, `EC2_USERNAME`, `EC2_SSH_KEY`.
- Required external runner labels: `self-hosted`, `linux`, `x64`, `devops-web-app-deploy`.
- Fixed release interfaces: workflow `CI`, branch `main`, repository `devops-web-app`, container `devops-web-app`, label `devops-web-app.version`, production host/container `80:5000`, local `5000:5000`, and health path `/health`.
- The Docker Hub public visibility choice is part of the baseline configuration, not merely documentation: EC2 has no registry-login path.

## Recommendations

1. Proceed to flow validation with the current MEDIUM risk classification and zero breaking changes.
2. Make the external acceptance boundary an explicit pre-production gate; do not convert local/offline evidence into hosted-service success claims.
3. Protect the self-hosted runner and `main` as production control-plane assets, require the `CI` check, and add a release-freshness/monotonicity guard so older successful runs cannot supersede newer releases.
4. Define whether `latest` means latest built candidate or latest healthy production release; avoid advancing a production alias before deployment acceptance.
5. Verify Git file mode, action/base-image provenance, published image digest/tag immutability, and the independently trusted SSH fingerprint during delivery hardening.
6. Treat route health semantics, `APP_VERSION`, workflow/runner/secret names, image/container identifiers, and port mappings as one versioned cross-file contract; add a raw-wire health regression test if the exact byte representation remains deployment-critical.
7. Retain a last-known-good image, serialize manual and automated host operations, rehearse manual full-SHA rollback, and monitor public reachability and post-deployment health beyond the script's bounded window.

## Sign-off

- **Risk level:** MEDIUM
- **Breaking changes:** 0
- **Direct impacts:** 8
- **Downstream impacts:** 7
- **Critical impact detected:** no
- **Proceed to flow validation:** yes
- **Residual limitation:** Git provenance/diff/mode and all hosted registry/runner/SSH/AWS behavior remain externally unverified.
