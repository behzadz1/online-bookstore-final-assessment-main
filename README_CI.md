# CI/CD (GitHub Actions)

This repository includes a fully automated **Continuous Integration / Continuous Deployment (CI/CD)** pipeline that validates code quality, security, and test coverage on every **push** and **pull request**.

## What It Does
- Installs dependencies and caches pip packages for faster runs.
- Lints the code using **flake8** for style and consistency.
- Runs security analysis with **bandit** to detect vulnerabilities.
- Executes **pytest** with coverage enforcement (minimum **90%**).
- Uploads test artifacts including:
  - `coverage.xml` (for Codecov or local analysis)
  - `reports/test-report.html` (HTML test summary)
  - `reports/htmlcov/` (coverage report)
- Uses matrix builds to test against **Python 3.10**, **3.11**, and **3.12**.
- Automatically skips redundant full runs for Dependabot PRs.

## Configuration Files
| File | Purpose |
|------|----------|
| `.github/workflows/CI.yml` | Main workflow automation script |
| `pytest.ini` | Defines coverage threshold and warnings control |
| `.coveragerc` | Excludes `tests/` and `profiles/` from coverage stats |
| `.flake8` | Linting and style rules |
| `Makefile` | Local developer automation tasks |
| `.github/dependabot.yml` | Automated dependency version checks |

## Local Usage
Run the same checks locally before pushing to GitHub:

```bash
make lint          # Run flake8 linting
make security      # Run bandit security scan
APP_ENV=test make test   # Run tests with coverage
# or directly
APP_ENV=test pytest -v --cov=. --cov-report=term-missing
```