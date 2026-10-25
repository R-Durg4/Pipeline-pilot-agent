# PipelinePilot — CI/CD Failure Analyzer

PipelinePilot is an independent portfolio project that demonstrates a small DevOps workflow: automated tests, a Docker image build, and a rule-based analyzer for common CI/CD log failures.

## Features

- Flask web interface for submitting a sanitized CI/CD log snippet.
- Rule-based detection for common dependency, test, permission, network, Docker, and memory-related failures.
- Troubleshooting suggestions for each detected pattern.
- Automated tests with `pytest`.
- GitHub Actions workflow that runs tests and builds the Docker image on pushes and pull requests to `main`.
- Dockerfile for repeatable packaging.

## Run locally

Requires Python 3.12 or compatible.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## Run tests

```bash
pytest -q
```

## Run with Docker

```bash
docker build -t pipelinepilot .
docker run --rm -p 5000:5000 pipelinepilot
```

Then open http://127.0.0.1:5000.

## CI workflow

`.github/workflows/ci.yml` runs on pushes and pull requests targeting `main`. It checks out the code, installs Python dependencies, runs the test suite, and builds a Docker image.

## Current scope and limitations

This is a learning/portfolio demo, not an autonomous remediation agent. It uses transparent text-matching rules; it does not connect to GitHub APIs, inspect real repositories, execute commands from submitted logs, change code, create branches, or open pull requests. Diagnoses are suggestions and must be verified by an engineer.

Do not paste secrets, tokens, customer data, or confidential logs into the application.

## Architecture

```text
Browser
  |
  v
Flask web interface
  |
  v
Rule-based log analyzer
  |
  v
Failure category + troubleshooting suggestions

GitHub push / pull request
  |
  v
GitHub Actions: install -> pytest -> Docker build
```

## Next improvements

- Add structured JSON output for CI jobs.
- Add sanitized example logs and additional tested detection rules.
- Add a deployment workflow after selecting a hosting platform.
- Add linting and dependency/security checks to CI.
