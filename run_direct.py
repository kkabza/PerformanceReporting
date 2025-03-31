#!/usr/bin/env python3
"""
Direct runner script for the Flask application that sets up logging
"""
import os
import sys
import logging
import datetime
from pathlib import Path

# Create instance/logs directory if it doesn't exist
instance_dir = Path('instance')
logs_dir = instance_dir / 'logs'
os.makedirs(logs_dir, exist_ok=True)

# Set up logging
current_date = datetime.datetime.now().strftime('%Y%m%d')
log_file = logs_dir / f'app_{current_date}.log.txt'

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('direct_runner')
logger.info('=============================================')
logger.info('Starting application with direct runner')
logger.info(f'Log file created at: {log_file}')

try:
    # Import the app module
    logger.info('Importing app.py...')
    import app as app_module
    
    # Get the Flask app using the create_app function from the module
    logger.info('Getting Flask app instance...')
    
    # Check if app_module defines create_app
    if hasattr(app_module, 'create_app'):
        logger.info('Using create_app factory function...')
        flask_app = app_module.create_app()
        logger.info('Created Flask app with factory')
    # Check if app_module defines app
    elif hasattr(app_module, 'app'):
        logger.info('Using app instance directly...')
        flask_app = app_module.app
    else:
        # Looking at the app.py code we know there's an 'app' variable assigned after create_app
        logger.info('Looking for app instance defined after create_app...')
        # Execute the app.py file directly
        logger.info('Running app.py to create app instance...')
        exec(open('app.py').read())
        # Now try to get the 'app' variable from globals
        if 'app' in globals():
            logger.info('Found app instance in globals...')
            flask_app = globals()['app']
        else:
            raise AttributeError("Could not find Flask app instance by any method")
    
    # Run the app on port 8080
    logger.info('Starting Flask app on port 8080...')
    flask_app.run(host='0.0.0.0', port=8080, debug=True)
    
except Exception as e:
    logger.error(f'Error starting the application: {str(e)}', exc_info=True)
    
    # Import app.py source code for debugging
    try:
        with open('app.py', 'r') as f:
            app_source = f.read()
            logger.info(f'app.py source (first 500 chars):\n{app_source[:500]}...')
    except Exception as file_err:
        logger.error(f'Could not read app.py: {file_err}')
    
    # Print instructions for fixing
    logger.info('Possible solutions:')
    logger.info('1. Check that app.py defines either an "app" variable or a create_app() function')
    logger.info('2. Ensure all dependencies are installed')
    logger.info('3. Check app/__init__.py to make sure it properly exports the app')
    
    sys.exit(1)

logger.info('Application exited normally') 