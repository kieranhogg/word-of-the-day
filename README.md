# Word of the Day

Word of the Day is a small API that gives children a new word each day. It also serves as a demo project for a DevOps deployment pipeline.

## Technologies

* Frontend: a single HTML file in `frontend/` using Alpine.js and Tailwind
* Backend: FastAPI in `api/`, run with uv and built into a Docker image
* Hosting: Caddy serves the frontend and proxies `/api/*` to the container on port 8000
* Servers: Terraform creates them (Proxmox for staging, Hetzner for production) and Ansible configures them
* CI/CD: GitHub Actions in `.github/workflows/`

## Running locally

```sh
uv sync
uv run fastapi dev api/main.py
uv run pytest
```

## API

* `GET /` returns today's word, with the level chosen from the day of the year
* `GET /{level}` returns today's word for `easy`, `medium`, `hard` or `complex`
* `GET /words/` returns every word
* `GET /words/random` returns one random word

## Files

* `.github/workflows/`
    * `tests.yml` runs pytest
    * `deploy-staging.yml` publishes the image, applies the staging Terraform and runs Ansible
    * `deploy-production.yml` does the same for production and runs only when started by hand
* `ansible/`
    * `setup.yml` prepares a fresh server
    * `deploy.yml` and `deploy-staging.yml` run every playbook in `playbooks/`
    * `staging.ini` is the staging inventory and `production.ini` is written by the production workflow
* `api/`
    * `data/` holds the word lists
    * `Dockerfile`
    * `main.py`
* `frontend/`
* `terraform/`
    * `production/` and `staging/` each hold `main.tf`, `variables.tf` and a `Caddyfile`
* `tests/`

## Secrets

`secrets.auto.tfvars` and `*.env` files are git ignored. The workflows read `TF_API_TOKEN`, `PROXMOX_TOKEN_ID`, `PROXMOX_TOKEN_SECRET`, `STAGING_SSH_KEY`, `PROD_SSH_KEY` and the `SSH_PUBLIC_KEY` variable from the repository settings.
