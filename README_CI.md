# CI/CD (GitHub Actions)

This repo includes a CI workflow that runs on every push and pull request.

## What it does
- Installs dependencies and caches pip
- Lints with **flake8**
- Runs security scan with **bandit**
- Executes **pytest** with coverage, enforcing **90%** minimum
- Uploads `coverage.xml` as an artifact

## Files
- `.github/workflows/CI.yml` — main workflow
- `pytest.ini` — pytest & coverage gate config
- `.coveragerc` — coverage include/exclude rules
- `.flake8` — linting rules
- `Makefile` — convenience tasks for local dev
- `.github/dependabot.yml` — automated dependency PRs

## Local usage
```bash
make lint
make security
APP_ENV=test make test
# or just
APP_ENV=test pytest
```

## Notes
- The workflow sets `APP_ENV=test` so any artificial delays are skipped in tests.
- Adjust `--cov-fail-under=` inside `pytest.ini` as your project evolves.
