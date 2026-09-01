# Flow Validation Report

**Workflow ID:** `c560efe0-973b-4512-81b9-66b879c0dd68`  
**Branch:** `containerized-web-app-cicd-pipeline` (planned branch; the physical workspace has no Git repository)  
**Flow Safety Score:** 80 / 100  
**Verdict:** REVIEW REQUIRED  
**Date:** `2026-08-31T13:03:58Z`

## Evidence basis

Flow validation independently read the live project-context README and all five MDC files, the RDD, the SDD, the PASS QA report, the MEDIUM impact-analysis report, the implementation summary, and the delivered application, templates, stylesheet, tests, container, Compose, CI, CD, deployment-script, dependency, pytest, and README files.

The current physical workspace is the implementation under review because Git is unavailable and no branch, commit, remote, or base-branch diff exists. This is a greenfield delivery: all three defined business flows are directly implemented by the change, so there are no non-impacted baseline flows.

Fresh local observation during this validation used the current files, not a prior image claim:

- `docker compose up -d --build` completed successfully and built `devops-web-app:local` from the current `Dockerfile` and source.
- `docker compose ps` reported the current service `Up ... (healthy)` with `5000:5000` published.
- Live `GET /`, `GET /about`, and `GET /health` each returned HTTP 200.
- The rendered home page contained `CI/CD Deployment Successful`, `Version 1.0.0`, and `/about` navigation targets; the About page contained its expected content and `/` return targets.
- The live health response was `application/json` with the exact command-substituted body `{"status":"healthy"}`.
- The temporary Compose container and network were removed after validation; `docker compose ps --all` was empty.

The PASS QA report supplies separate execution evidence for 12/12 pytest tests through all three entry commands, Docker image/runtime inspection, Compose startup, live route probes, workflow parsing, Bash syntax, exact/malformed health-body checks, and controlled offline deployment/rollback scenarios. It explicitly states that hosted GitHub Actions, Docker Hub, the self-hosted runner, SSH, and AWS EC2 were not exercised.

## Impacted Flows

| Flow | ID | Criticality | Status | Evidence |
|------|----|-------------|--------|----------|
| Browse portfolio web application | `browse-portfolio-app` | medium | `UNAFFECTED` | `app.py:27-36` implements both entry points; `templates/base.html:12-20`, `templates/index.html:14-19`, and `templates/about.html:31-36` connect Home and About navigation. Fresh current-image Compose probes returned HTTP 200 for both pages, rendered the required success/version content, and exposed the expected link targets. `tests/test_app.py:15-36,46-71` and the PASS QA report provide deterministic route/content/version/escaping regression evidence. No broken navigation or presentation dependency was observed. |
| Monitor application health | `monitor-application-health` | high | `AT_RISK` | `app.py:38-40` returns HTTP 200 healthy JSON. The Docker image, Compose, CI, and EC2 script consume the same route at `Dockerfile:26-27`, `docker-compose.yml:10-20`, `.github/workflows/ci.yml:63-93`, and `scripts/deploy.sh:97-140`. Fresh current-image validation observed Docker `healthy` plus HTTP 200, `application/json`, and the exact body `{"status":"healthy"}`. QA also verified parsed JSON and the corrected fail-closed Bash comparison, including rejection of `{"status":"heal thy"}`. However, the hosted CI consumer, real EC2 loopback/public-port consumer, and live rollback health path were not exercised; the impact report also identifies exact-byte coupling and the absence of continuous post-deployment monitoring. Strong local evidence avoids `UNKNOWN` or `LIKELY_BROKEN`, but these high-criticality production gaps require `AT_RISK`. |
| Build and deploy a verified container | `automated-container-deployment` | high | `AT_RISK` | CI and CD source implement the declared gate, build, dual tags, labeled runner, and SSH handoff (`.github/workflows/ci.yml:3-113`; `.github/workflows/cd.yml:3-150`). The deployment script implements pre-mutation pull, prior-image capture, `80:5000`, bounded exact health verification, rollback, and first-deploy handling (`scripts/deploy.sh:62-95,97-140,164-245,260-327`). PASS QA records local workflow/static checks and controlled offline deployment/rollback scenarios. However, no hosted workflow, target Docker Hub push/pull, runner job, SSH connection, or EC2 deploy/rollback has run. The MEDIUM impact report also identifies non-monotonic release ordering, separately rebuilt and overwriteable SHA tags, first-contact `ssh-keyscan` trust, and `latest` publication before deployed-health acceptance. These are concrete regression risks, but no evidence establishes that the flow is already `LIKELY_BROKEN`. |

## Non-Impacted Flows

| Flow | ID | Status |
|------|----|--------|
| None | N/A | All three live MDC flows are directly created or consumed by this greenfield change. |

## Regression Recommendation

| Flow | Recommended regression |
|------|------------------------|
| `browse-portfolio-app` | Keep the route/content/version tests and current-image container smoke. Add an explicit rendered-link target or browser-click assertion and a small responsive-browser smoke check when browser automation is introduced. |
| `monitor-application-health` | Keep pytest, image-health, Compose, CI, and exact raw-body deployment checks together. In external acceptance, verify the EC2 loopback endpoint and the public port-80 endpoint, and add continuous external health monitoring because deployment-time checks do not cover later degradation. |
| `automated-container-deployment` | Treat the first real pipeline as a production acceptance gate: require hosted CI for the exact current `main` SHA; prove the labeled dedicated runner and controlled egress; record Docker Hub `latest` and full-SHA tags plus digest/public pull; verify an independently trusted SSH host fingerprint; deploy to EC2; verify loopback and public port 80 plus displayed SHA version; and exercise a sanitized failed-health rollback. Add a current-`main`/monotonic-release guard and prevent or detect SHA-tag overwrite before accepting the release path as hardened. |

## External acceptance boundary

| Boundary | Observed local/source evidence | External acceptance status | Required evidence |
|----------|--------------------------------|----------------------------|-------------------|
| Hosted GitHub CI/CD | Workflow YAML parsed in QA; substantive CI commands and gates were exercised locally; source gates on a successful same-repository push CI run. | **NOT RUN / NOT ACCEPTED** | Hosted run/check URLs for the exact current `main` SHA, including CI container smoke, CD trigger, and final job result. |
| Docker Hub | CD declares login and one build publishing `latest` plus the full SHA; the host script pulls before mutation. | **NOT RUN / NOT ACCEPTED** | Sanitized login/push evidence, both target tags, recorded digest, public pull from the intended namespace, and confirmation that a SHA tag cannot silently change. |
| Self-hosted deployment runner | CD selects `self-hosted`, `linux`, `x64`, and `devops-web-app-deploy`; README defines trusted dedicated-runner and controlled-egress requirements. | **NOT REGISTERED OR EXERCISED IN EVIDENCE** | Runner registration, label match, required tools, repository isolation, service health, and egress IP matching the EC2 SSH `/32`. |
| SSH host boundary | CD validates a temporary `0600` key and enables strict host checking with bounded SSH settings. | **NOT CONNECTED / NOT ACCEPTED** | Successful connection from the intended runner and comparison with an independently trusted EC2 host fingerprint; `ssh-keyscan` discovery alone is trust on first use. |
| AWS EC2 runtime | Script and offline scenarios cover replacement, exact local health, rollback, and `80:5000`; the application container is locally healthy. | **NOT DEPLOYED / NOT ACCEPTED** | Real EC2 pull/start, Docker and loopback health, public port-80 page/health/version, security-group validation, repeat deployment, failed-release rollback, and first-deploy recovery evidence. |

The repository therefore demonstrates local/source completeness but does not demonstrate a successful hosted or production deployment. This report does not convert local or offline checks into GitHub, Docker Hub, runner, SSH, or EC2 success claims.

## Risk Assessment

- `browse-portfolio-app` has direct current-image and automated evidence across both entry points. Navigation was validated through rendered link targets and successful target requests; no JavaScript or external presentation dependency exists.
- `monitor-application-health` is high-criticality and `AT_RISK`. It has direct current-image evidence and consistent consumers across Docker, Compose, CI, and deployment, so it is neither `UNKNOWN` nor `LIKELY_BROKEN`. The hosted CI consumer, EC2 loopback/public-path consumer, and live rollback health path remain unaccepted; the exact-byte EC2 comparison is a fragile coordinated contract, and no continuous monitor covers degradation after the bounded deployment window.
- `automated-container-deployment` is high-criticality and `AT_RISK` because its external half has never run and the impact report identifies release-order, artifact-identity, host-trust, and registry-state hazards. Source/offline evidence is strong enough to avoid `UNKNOWN`, while the absence of a failing external run or a proven deterministic break avoids `LIKELY_BROKEN`.
- The impact-analysis risk level is `MEDIUM`, with zero breaking changes. Under the prescribed scoring rules, MEDIUM itself has no score deduction.
- There are no migrations, schemas, persistent data, authenticated application actions, or pre-existing consumers to regress.

## Score breakdown

Start at **100**.

| Condition | Count | Deduction |
|-----------|------:|----------:|
| `LIKELY_BROKEN`, high criticality | 0 | 0 |
| `LIKELY_BROKEN`, medium/low criticality | 0 | 0 |
| `AT_RISK`, high criticality (`monitor-application-health`, `automated-container-deployment`) | 2 | -20 |
| `UNKNOWN` | 0 | 0 |
| Impact report `CRITICAL` | 0 | 0 |
| Impact report `HIGH` | 0 | 0 |
| Impact report `MEDIUM` | 1 | 0 |
| **Final Flow Safety Score** |  | **80 / 100** |

Score `80` is in the `61-80` REVIEW REQUIRED band, so the handoff is `READY_FOR_REVIEW` with `reviewRequired: true`.

## Sign-off

- **Flow Validation Agent:** independent physical-workspace and current-image validation
- **Status:** `READY_FOR_REVIEW`
- **Review required by score:** yes
- **Impacted flow IDs:** `browse-portfolio-app`, `monitor-application-health`, `automated-container-deployment`
- **Non-impacted flow count:** 0
- **Production acceptance:** pending for hosted GitHub Actions, Docker Hub, the self-hosted runner, SSH, and AWS EC2
