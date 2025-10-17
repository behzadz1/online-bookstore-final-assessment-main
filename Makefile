# Convenience targets for local dev
.PHONY: test lint security ci

test:
	APP_ENV=test pytest

lint:
	flake8 .

security:
	bandit -q -r .

ci: lint security test
