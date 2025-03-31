"""
Report Enforcer - Ensures build reports are never skipped.
This module enforces the TDD cursor rule requiring test summaries.
"""
import os
import time
import atexit
import datetime
import subprocess
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("report_enforcer")

class ReportEnforcer:
    """Enforces the creation of build reports per TDD cursor rules"""
    
    def __init__(self):
        """Initialize the report enforcer"""
        self.reports_dir = Path('build_reports')
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.session_start = datetime.datetime.now()
        self.report_generated = False
        
        # Register exit handler to ensure report is created
        atexit.register(self.ensure_report_on_exit)
        
        # Create initial report marker
        self._create_session_marker()
        logger.info("Report enforcer initialized - build reports will be enforced")

    def _create_session_marker(self):
        """Create a session marker file to track the current session"""
        marker_file = self.reports_dir / f".session_{int(time.time())}"
        with open(marker_file, 'w') as f:
            f.write(f"Session started: {self.session_start.isoformat()}\n")
            f.write(f"PID: {os.getpid()}\n")
    
    def ensure_report_on_exit(self):
        """Ensure a report is generated when the program exits"""
        if not self.report_generated:
            logger.warning("No build report was generated during this session! Generating one now...")
            try:
                from app.utils.test_reporter import create_build_report
                report_path = create_build_report("auto-generated")
                logger.info(f"Auto-generated build report at: {report_path}")
                self.report_generated = True
            except Exception as e:
                # If the import fails, use a more direct approach as fallback
                logger.error(f"Error importing test_reporter: {e}")
                self._generate_fallback_report()
    
    def _generate_fallback_report(self):
        """Generate a fallback report if the normal method fails"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        report_path = self.reports_dir / f'test-summary-{timestamp}.txt'
        
        with open(report_path, 'w') as f:
            f.write("====================================\n")
            f.write("Florida Tax Certificate Sales Test Summary\n")
            f.write("====================================\n\n")
            f.write(f"Test Run Start Time: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Test Run End Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Total Tests Run: (unknown - fallback report)\n")
            f.write("Passed: (unknown - fallback report)\n")
            f.write("Failed: (unknown - fallback report)\n")
            f.write("Skipped: (unknown - fallback report)\n\n")
            f.write("Test Coverage Summary:\n")
            f.write("---------------------\n")
            f.write("Fallback report generated - no test data available\n\n")
            f.write("Notes on Test Modifications:\n")
            f.write("---------------------------\n")
            f.write("ATTENTION: This is a fallback report generated because no proper report was created.\n")
            f.write("⚠️ TDD VIOLATION: Build reports must be explicitly generated for each session.\n\n")
            f.write(f"Executed By: {os.environ.get('USER', 'Unknown')}\n")
            try:
                result = subprocess.run(['git', 'describe', '--always', '--dirty'], 
                                       capture_output=True, text=True, check=False)
                version = result.stdout.strip() if result.returncode == 0 else "Unknown"
            except Exception:
                version = "Unknown"
            f.write(f"Build Version: {version}\n")
        
        logger.info(f"Generated fallback report at: {report_path}")
        self.report_generated = True
        
    def mark_report_generated(self):
        """Mark that a report has been properly generated"""
        self.report_generated = True
        logger.info("Build report has been marked as generated")

# Create a singleton instance
enforcer = ReportEnforcer()

# Expose key functions at module level
def mark_report_generated():
    """Mark that a report has been properly generated in this session"""
    enforcer.mark_report_generated()

def enforce_report_generation():
    """Force a report to be generated immediately"""
    if not enforcer.report_generated:
        enforcer.ensure_report_on_exit()
    return enforcer.report_generated 