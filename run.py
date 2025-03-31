#!/usr/bin/env python3
"""
Startup script for Florida Tax Certificate Sale Auctions web application.
Follows Cursor rules and establishes proper logging and test structures.
"""
import os
import sys
import logging
import datetime
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

def run_app():
    """Run the Flask application"""
    logger.info('Initializing Flask application')
    
    # Import the Flask app module
    # Our app is defined directly in app.py, not as a module inside app/
    import app as flask_app
    
    # Set debug mode from environment variable
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    # Check blueprint URL rules
    check_blueprint_url_rules()
    
    # Check UI accessibility
    check_ui_accessibility()
    
    logger.info(f'Running Flask app in {"development" if debug else "production"} mode')
    
    # Run the application
    flask_app.app.run(host='0.0.0.0', port=5000, debug=debug)

if __name__ == '__main__':
    log_dir = setup_directories()
    logger = setup_logging(log_dir)
    
    try:
        run_app()
    except Exception as e:
        logger.error(f'Error in application: {str(e)}', exc_info=True)
        sys.exit(1) 