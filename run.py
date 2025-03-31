#!/usr/bin/env python3
"""
Startup script for Florida Tax Certificate Sale Auctions web application.
Follows Cursor rules and establishes proper logging and test structures.
"""
import os
import sys
import logging
import datetime
import time
import requests
import subprocess
from pathlib import Path
from flask import Flask

# Create necessary directories for logs and tests
def setup_directories():
    # Ensure log directory exists with proper structure
    log_dir = Path('instance/logs')
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Ensure test directories exist per TDD rule
    test_dirs = [
        'tests/bdd',
        'tests/unit',
        'tests/functional',
        'tests/integration',
        'tests/sql',
        'tests/api',
        'tests/ui'
    ]
    for test_dir in test_dirs:
        Path(test_dir).mkdir(parents=True, exist_ok=True)
    
    # Create an empty __init__.py in tests directory to make it a package
    Path('tests/__init__.py').touch(exist_ok=True)
    
    # Create build_reports directory
    reports_dir = Path('build_reports')
    reports_dir.mkdir(exist_ok=True)
    
    return log_dir

# Configure logging according to the logging-architecture rule
def setup_logging(log_dir):
    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    log_file = log_dir / f'app_{timestamp}.log.txt'
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger('taxsale')
    logger.info('Starting Florida Tax Certificate Sale Auctions application')
    
    return logger

def check_blueprint_url_rules():
    """Verify blueprint URL rules are correctly prefixed"""
    logger.info('Checking blueprint URL rules...')
    for root, dirs, files in os.walk('app/templates'):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r') as f:
                    content = f.read()
                    # This is a simple check for unprefixed url_for calls
                    if "url_for('" in content and "url_for('home." not in content and "url_for('static" not in content:
                        logger.warning(f'Possible unprefixed url_for in {path}')

def check_ui_accessibility():
    """Check for potential accessibility issues in templates"""
    logger.info('Checking UI accessibility standards...')
    problematic_combos = [
        ('text-gray-300', 'bg-white'),
        ('text-blue-900', 'bg-black'),
        ('text-yellow-300', 'bg-white')
    ]
    
    for root, dirs, files in os.walk('app/templates'):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r') as f:
                    content = f.read()
                    for combo in problematic_combos:
                        if combo[0] in content and combo[1] in content:
                            logger.warning(f'Possible accessibility contrast issue in {path}: {combo[0]} with {combo[1]}')

def ensure_build_reports():
    """Ensure build reports are generated according to TDD cursor rules"""
    logger.info('Checking for build reports...')
    
    # We need to add the current directory to the Python path to ensure imports work
    sys.path.insert(0, os.getcwd())
    
    try:
        # First check if a recent build report exists
        reports_dir = Path('build_reports')
        reports = list(reports_dir.glob('test-summary-*.txt'))
        
        # Sort reports by creation time, newest first
        reports.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        
        # Check if the most recent report is less than 24 hours old
        if reports and (datetime.datetime.now().timestamp() - reports[0].stat().st_mtime) < 86400:
            logger.info(f'Recent build report found: {reports[0]}')
            with open(reports[0], 'r') as f:
                logger.info(f'Report summary: {f.readline().strip()}')
        else:
            # No recent reports, generate one
            logger.info('No recent build reports found, generating new report...')
            from app.utils.test_reporter import create_build_report
            report_path = create_build_report("pre-build")
            logger.info(f'Generated new build report: {report_path}')
    
    except Exception as e:
        logger.error(f'Error ensuring build reports: {str(e)}', exc_info=True)
        # Continue app execution even if report generation fails

def verify_home_page_loads(port=5000, max_attempts=10, wait_time=1):
    """
    Verify that the home page loads correctly after startup.
    This is a critical post-build test required by the TDD cursor rules.
    """
    logger.info("Performing post-build test: Verifying home page loads...")
    
    # The URL to check
    url = f"http://localhost:{port}"
    
    # Give the server a moment to start up
    time.sleep(2)
    
    # Try to access the home page multiple times
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                logger.info(f"✅ Home page loaded successfully (HTTP {response.status_code})!")
                
                # Check if the page contains expected content
                if "Florida Tax Certificate" in response.text:
                    logger.info("✅ Home page contains expected content!")
                    return True
                else:
                    logger.warning("❌ Home page does not contain expected content!")
            else:
                logger.warning(f"❌ Home page returned HTTP {response.status_code}")
                
            # If we didn't return True yet, try again after waiting
            time.sleep(wait_time)
            
        except requests.RequestException as e:
            logger.warning(f"❌ Error accessing home page (attempt {attempt+1}/{max_attempts}): {str(e)}")
            time.sleep(wait_time)
    
    # If we get here, all attempts failed
    logger.error("❌ Failed to verify home page loads after multiple attempts!")
    return False

def run_app():
    """Run the Flask application"""
    logger.info('Initializing Flask application')
    
    # We need to add the current directory to the Python path to ensure imports work
    sys.path.insert(0, os.getcwd())
    
    # Make sure we have proper build reports before starting
    ensure_build_reports()
    
    try:
        # Try to import the Flask app from app.py
        import app
        logger.info("Successfully imported app module")
        
        # Set debug mode from environment variable
        debug = os.environ.get('FLASK_ENV') == 'development'
        
        # Check blueprint URL rules
        check_blueprint_url_rules()
        
        # Check UI accessibility
        check_ui_accessibility()
        
        logger.info(f'Running Flask app in {"development" if debug else "production"} mode')
        
        # Start the application in a subprocess so we can continue executing this script
        flask_process = subprocess.Popen(
            [sys.executable, "-c", 
            "import app; app.app.run(debug=True, host='0.0.0.0', port=5000)"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Verify home page loads as a post-build test
        success = verify_home_page_loads()
        
        if success:
            logger.info("Post-build test passed: Home page is accessible")
            # Continue running the app in the main thread
            logger.info("Continuing with main application thread")
            
            # Kill the subprocess now that we've verified it's working
            flask_process.terminate()
            
            # Run the application directly in this process
            app.app.run(host='0.0.0.0', port=5000, debug=True)
        else:
            logger.error("Post-build test failed: Home page is not accessible!")
            logger.error("Terminating application due to failed post-build test")
            
            # Kill the flask process
            flask_process.terminate()
            sys.exit(1)
    
    except ImportError as e:
        logger.error(f"Failed to import app module: {str(e)}")
        sys.exit(1)
    except AttributeError as e:
        logger.error(f"Failed to access app instance: {str(e)}")
        # Let's see what attributes are available in the app module
        logger.info(f"Available attributes in app module: {dir(app)}")
        sys.exit(1)

if __name__ == '__main__':
    log_dir = setup_directories()
    logger = setup_logging(log_dir)
    
    try:
        run_app()
    except Exception as e:
        logger.error(f'Error in application: {str(e)}', exc_info=True)
        sys.exit(1) 