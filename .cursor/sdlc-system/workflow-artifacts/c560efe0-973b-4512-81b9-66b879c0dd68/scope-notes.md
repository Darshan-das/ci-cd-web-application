# Scope notes

- **Repository:** current workspace (`.`), the only modifiable repository.
- **Application:** `app.py`, `templates/`, and `static/` implement three stateless Flask routes and environment-driven version rendering.
- **Tests:** `tests/` covers route status, health JSON, and version behavior without network access.
- **Runtime:** `requirements.txt`, `Dockerfile`, `.dockerignore`, and `docker-compose.yml` define Python 3.12, Gunicorn, non-root execution, port 5000, and local health checks.
- **Automation:** `.github/workflows/ci.yml` validates tests and a running container; `.github/workflows/cd.yml` publishes `latest` plus immutable SHA tags and deploys over SSH only after validation.
- **Production deployment:** `scripts/deploy.sh` maps host port 80 to container port 5000, retains the previous local image ID, verifies health, and attempts rollback on failure.
- **Security:** no credentials are written to files; GitHub Secrets supply Docker Hub and EC2 values; EC2 documentation limits public ingress to HTTP 80 and source-restricted SSH 22.
- **Explicit exclusions:** Kubernetes, Terraform, ArgoCD, live infrastructure provisioning, TLS, multi-host scaling, zero-downtime deployment, and unverified success claims.
