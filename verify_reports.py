#!/usr/bin/env python3
"""
Build Report Verification Script
Ensures that proper build reports exist for the Florida Tax Certificate Sale application.
This tool should be used to explicitly check for compliant build reports.
"""
import os
import sys
import glob
import datetime
from pathlib import Path

# ANSI color codes for formatting output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
END = '\033[0m'

def print_error(message):
    """Print an error message in red"""
    print(f"{RED}{BOLD}ERROR:{END} {RED}{message}{END}")

def print_warning(message):
    """Print a warning message in yellow"""
    print(f"{YELLOW}{BOLD}WARNING:{END} {YELLOW}{message}{END}")

def print_success(message):
    """Print a success message in green"""
    print(f"{GREEN}{BOLD}SUCCESS:{END} {GREEN}{message}{END}")

def check_build_reports():
    """Check if proper build reports exist"""
    print(f"\n{BOLD}Checking build reports for TDD compliance...{END}\n")
    
    reports_dir = Path('build_reports')
    
    # Check if the directory exists
    if not reports_dir.exists():
        print_error(f"Build reports directory '{reports_dir}' does not exist!")
        print("Creating directory...")
        reports_dir.mkdir(parents=True, exist_ok=True)
        print_warning("No build reports found. TDD rules are being violated!")
        return False
    
    # Find all build reports
    report_files = list(reports_dir.glob('test-summary-*.txt'))
    if not report_files:
        print_error("No build reports found! TDD rules are being violated!")
        return False
    
    # Sort by creation time, newest first
    report_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    
    # Check the most recent report
    latest_report = report_files[0]
    mod_time = latest_report.stat().st_mtime
    now = datetime.datetime.now().timestamp()
    
    # Get the age of the latest report
    age_hours = (now - mod_time) / 3600
    
    print(f"Latest build report: {latest_report.name}")
    print(f"Created: {datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Age: {age_hours:.1f} hours")
    
    # Check the content of the latest report for required fields
    with open(latest_report, 'r') as f:
        content = f.read()
        
        # Check for required content
        missing_fields = []
        for field in [
            "Test Run Start Time", 
            "Test Run End Time", 
            "Total Tests Run", 
            "Passed", 
            "Failed", 
            "Test Coverage Summary", 
            "Notes on Test Modifications"
        ]:
            if field not in content:
                missing_fields.append(field)
        
        if missing_fields:
            print_warning(f"Latest report is missing required fields: {', '.join(missing_fields)}")
            print_warning("This violates the TDD report content requirements!")
        else:
            print_success("Latest report contains all required fields")
    
    # If the latest report is older than 24 hours, warn the user
    if age_hours > 24:
        print_warning(f"Latest report is more than 24 hours old ({age_hours:.1f} hours)")
        print_warning("You should generate a new report for the current session!")
        return False
    else:
        print_success(f"Latest report is recent ({age_hours:.1f} hours old)")
    
    # Report on all available reports
    print(f"\nFound {len(report_files)} build reports in total")
    
    # All checks passed
    if age_hours <= 24 and not missing_fields:
        print_success("Build report compliance verified! TDD rules are being followed.")
        return True
    else:
        print_warning("Build reports need attention. Please run 'make report' to generate a new report.")
        return False

def force_report_generation():
    """Force the generation of a new build report"""
    print(f"\n{BOLD}Forcing build report generation...{END}\n")
    
    try:
        # Add the current directory to the Python path
        sys.path.insert(0, os.getcwd())
        
        # Try to import the report enforcer
        try:
            from app.utils import report_enforcer
            report_enforcer.enforce_report_generation()
            print_success("Build report successfully generated using report enforcer")
            return True
        except ImportError:
            # Fall back to the test reporter
            try:
                from app.utils.test_reporter import create_build_report
                report_path = create_build_report("manually-generated")
                print_success(f"Build report successfully generated: {report_path}")
                return True
            except ImportError:
                print_error("Could not import test_reporter module!")
                return False
    except Exception as e:
        print_error(f"Failed to generate build report: {str(e)}")
        return False

def main():
    """Main function"""
    print(f"{BOLD}Florida Tax Certificate Sale - Build Report Verification{END}")
    print(f"{BOLD}==================================================={END}")
    
    # Check if we want to force generation
    if len(sys.argv) > 1 and sys.argv[1] == '--force':
        force_report_generation()
    
    # Always check the reports
    check_build_reports()

if __name__ == "__main__":
    main() 