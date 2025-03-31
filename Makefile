.PHONY: help clean test report pre-build-test post-build-test lint run debug init verify-reports force-report commit-check

help:
	@echo "Available commands:"
	@echo "  make clean           - Remove temporary files"
	@echo "  make test            - Run tests"
	@echo "  make report          - Generate test report"
	@echo "  make pre-build-test  - Run pre-build tests"
	@echo "  make post-build-test - Run post-build tests"
	@echo "  make lint            - Run linter"
	@echo "  make run             - Run the application"
	@echo "  make debug           - Run the application in debug mode"
	@echo "  make init            - Initialize the project"
	@echo "  make verify-reports  - Check if build reports exist and are valid"
	@echo "  make force-report    - Force generate a new build report"
	@echo "  make commit-check    - Check for uncommitted changes"
	@echo "  make tdd-compliance  - Verify TDD compliance"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name "*.eggs" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".tox" -exec rm -rf {} +
	find . -type d -name ".hypothesis" -exec rm -rf {} +

test:
	python3 -m pytest -v

report:
	@echo "Generating test report..."
	@echo "Running unit tests for report..."
	python3 -m pytest -v --cov=app tests/unit
	@echo "Report generation complete."

pre-build-test:
	@echo "Running pre-build tests..."
	python3 -m pytest tests/unit/
	python3 -m pytest tests/sql/
	python3 -m pytest tests/bdd/
	@echo "Pre-build tests complete."

post-build-test:
	@echo "Running post-build tests..."
	python3 -m pytest tests/integration/
	python3 -m pytest tests/functional/
	python3 -m pytest tests/api/
	python3 -m pytest tests/ui/
	@echo "Post-build tests complete."

lint:
	pylint app

run:
	python3 run.py

debug:
	FLASK_ENV=development FLASK_DEBUG=1 python3 run.py

init:
	pip3 install -r requirements.txt

verify-reports:
	./verify_reports.py

force-report:
	./verify_reports.py --force
	
commit-check:
	@echo "Checking for uncommitted changes..."
	./check_for_uncommitted.py

tdd-compliance: verify-reports pre-build-test
	@echo "TDD compliance verified." 