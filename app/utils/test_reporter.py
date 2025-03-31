"""
Test reporting utility for Florida Tax Certificate Sale Auctions.
Follows TDD cursor rules for proper test reporting.
"""
import os
import sys
import datetime
import inspect
import subprocess
from pathlib import Path


class TestReporter:
    """Handles test reporting according to TDD cursor rules"""
    
    def __init__(self):
        """Initialize the test reporter"""
        self.report_dir = Path('build_reports')
        self.report_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        self.report_path = self.report_dir / f'test-summary-{self.timestamp}.txt'
        self.start_time = datetime.datetime.now()
        self.end_time = None
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.tests_skipped = 0
        self.coverage_summary = ""
        self.modification_notes = ""

    def pre_test_report(self, test_type="pre-build"):
        """Generate a pre-test report"""
        with open(self.report_path, 'w') as report_file:
            report_file.write(self._get_report_header())
            report_file.write(f"\nTest Run Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            report_file.write(f"Test Type: {test_type} tests\n")
            report_file.write("\nPre-build tests to be run:\n")
            report_file.write("- Unit tests\n")
            report_file.write("- SQL tests\n")
            report_file.write("- BDD tests\n\n")
            report_file.write("Status: PENDING\n\n")
            
        return self.report_path
    
    def post_test_report(self, test_type="post-build", modification_notes="", test_status=None):
        """Generate a post-test report with results"""
        self.end_time = datetime.datetime.now()
        self.modification_notes = modification_notes
        
        if test_status:
            self.tests_run = test_status.get('total', 0)
            self.tests_passed = test_status.get('passed', 0)
            self.tests_failed = test_status.get('failed', 0)
            self.tests_skipped = test_status.get('skipped', 0)
        
        # Run pytest with coverage to get coverage summary
        try:
            result = subprocess.run(
                ['pytest', '--cov=app', '--cov-report=term'],
                capture_output=True,
                text=True
            )
            coverage_output = result.stdout.strip()
            
            # Extract the coverage summary section
            if 'TOTAL' in coverage_output:
                lines = coverage_output.split('\n')
                for i, line in enumerate(lines):
                    if 'TOTAL' in line:
                        self.coverage_summary = '\n'.join(lines[i-10:i+1])
                        break
        except Exception as e:
            self.coverage_summary = f"Error generating coverage: {str(e)}"
        
        with open(self.report_path, 'w') as report_file:
            report_file.write(self._get_report_header())
            report_file.write(f"\nTest Run Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            report_file.write(f"Test Run End Time: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            report_file.write(f"Duration: {(self.end_time - self.start_time).total_seconds():.2f} seconds\n\n")
            
            report_file.write(f"Total Tests Run: {self.tests_run}\n")
            report_file.write(f"Passed: {self.tests_passed}\n")
            report_file.write(f"Failed: {self.tests_failed}\n")
            report_file.write(f"Skipped: {self.tests_skipped}\n\n")
            
            report_file.write("Test Coverage Summary:\n")
            report_file.write("---------------------\n")
            report_file.write(f"{self.coverage_summary}\n\n")
            
            report_file.write("Notes on Test Modifications:\n")
            report_file.write("---------------------------\n")
            report_file.write(f"{self.modification_notes or 'No modifications noted.'}\n\n")
            
            report_file.write(f"Executed By: {os.environ.get('USER', 'Unknown')}\n")
            report_file.write(f"Build Version: {self._get_git_version()}\n")
        
        return self.report_path
    
    def _get_report_header(self):
        """Get the report header"""
        return """====================================
Florida Tax Certificate Sales Test Summary
====================================
"""
    
    def _get_git_version(self):
        """Get the git version information"""
        try:
            result = subprocess.run(
                ['git', 'describe', '--always', '--dirty'],
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except Exception:
            return "Unknown"
    
    def run_tests(self, test_type="all"):
        """Run tests and generate a report"""
        self.pre_test_report(test_type)
        
        test_status = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0
        }
        
        try:
            if test_type == "pre-build":
                test_categories = ["unit", "sql", "bdd"]
            elif test_type == "post-build":
                test_categories = ["integration", "functional", "api", "ui"]
            else:
                test_categories = ["unit", "integration", "functional", "sql", "api", "ui", "bdd"]
            
            # Run each test category
            for category in test_categories:
                test_dir = Path(f"tests/{category}")
                if test_dir.exists() and any(test_dir.glob('test_*.py')):
                    print(f"Running {category} tests...")
                    result = subprocess.run(
                        ['pytest', f'tests/{category}', '-v'],
                        capture_output=True,
                        text=True
                    )
                    
                    # Parse results to update test status
                    last_line = result.stdout.strip().split('\n')[-1] if result.stdout else ""
                    if "passed" in last_line or "failed" in last_line:
                        parts = last_line.split(',')
                        for part in parts:
                            part = part.strip()
                            if "passed" in part:
                                test_status['passed'] += int(part.split()[0])
                                test_status['total'] += int(part.split()[0])
                            elif "failed" in part:
                                test_status['failed'] += int(part.split()[0])
                                test_status['total'] += int(part.split()[0])
                            elif "skipped" in part:
                                test_status['skipped'] += int(part.split()[0])
                                test_status['total'] += int(part.split()[0])
            
            modification_notes = f"Test run completed for {test_type} test categories: {', '.join(test_categories)}"
            
        except Exception as e:
            modification_notes = f"Error running tests: {str(e)}"
        
        return self.post_test_report(
            test_type=test_type,
            modification_notes=modification_notes,
            test_status=test_status
        )


def create_build_report(test_type="all"):
    """Factory function to create a build report"""
    reporter = TestReporter()
    return reporter.run_tests(test_type) 