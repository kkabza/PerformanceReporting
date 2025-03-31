.PHONY: run install clean test test-unit test-all report

run:
	python run.py

install:
	pip install -r requirements.txt

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov

test-unit:
	pytest tests/unit -v

test-integration:
	pytest tests/integration -v

test-functional:
	pytest tests/functional -v

test-api:
	pytest tests/api -v

test-ui:
	pytest tests/ui -v

test-sql:
	pytest tests/sql -v

test-bdd:
	pytest tests/bdd -v

test:
	pytest

test-all: test-unit test-integration test-functional test-api test-ui test-sql test-bdd
	@echo "All tests completed"

report:
	python -c "import datetime; print('Report generated at: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))" > build_reports/test-summary-$$(date +"%Y%m%d-%H%M%S").txt
	pytest --cov=app --cov-report=term >> build_reports/test-summary-$$(date +"%Y%m%d-%H%M%S").txt 