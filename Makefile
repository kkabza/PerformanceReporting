.PHONY: run install clean test test-unit test-all report pre-build-test post-build-test report-status

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
	python -c "from app.utils.test_reporter import create_build_report; print(create_build_report('all'))"

pre-build-test:
	python -c "from app.utils.test_reporter import create_build_report; print(create_build_report('pre-build'))"

post-build-test:
	python -c "from app.utils.test_reporter import create_build_report; print(create_build_report('post-build'))"

report-status:
	@echo "Checking for build reports..."
	@ls -lt build_reports/ | head -5 