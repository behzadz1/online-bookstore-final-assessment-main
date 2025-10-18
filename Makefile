.PHONY: test lint coverage report clean

test:
	pytest -q --disable-warnings --cov=. --cov-report=term-missing

lint:
	flake8 .

coverage:
	pytest -q --disable-warnings --cov=. --cov-report=html:reports/htmlcov

report:
	pytest -v --html=reports/test-report.html --self-contained-html

clean:
	rm -rf __pycache__ .pytest_cache .coverage reports/
