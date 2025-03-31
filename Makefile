.PHONY: run install clean test test-unit test-all report pre-build-test post-build-test report-status verify-reports force-report

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

# !!! CRITICAL: TDD RULE - NEVER SKIP REPORTS !!!
report:
	@echo "Generating build report..."
	@python -c "from app.utils.test_reporter import create_build_report; print(create_build_report('all'))"
	@echo "Build report generated successfully!"

pre-build-test:
	@echo "Running pre-build tests and generating report..."
	@python -c "from app.utils.test_reporter import create_build_report; print(create_build_report('pre-build'))"
	@echo "Pre-build tests completed and report generated."

post-build-test:
	@echo "Running post-build tests and generating report..."
	@python -c "from app.utils.test_reporter import create_build_report; print(create_build_report('post-build'))"
	@echo "Post-build tests completed and report generated."

report-status:
	@echo "Checking for build reports..."
	@ls -lt build_reports/ | head -5

verify-reports:
	@python verify_reports.py

force-report:
	@python verify_reports.py --force

# Special target to help comply with TDD rules
tdd-compliance: verify-reports pre-build-test
	@echo "TDD compliance check completed." 