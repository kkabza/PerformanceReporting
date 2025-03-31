#!/usr/bin/env python3
"""
Script to start the Flask application on port 8080
This script imports the app instance from app.py
"""
import os
import logging
import sys

# Configure logging early
os.makedirs('instance/logs', exist_ok=True)
log_filename = os.path.join('instance/logs', f"app_{os.getenv('FLASK_ENV', 'development')}.log.txt")

# Set up logger before importing app
logger = logging.getLogger('start_app')
handler = logging.FileHandler(log_filename)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter(
    '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.info('=== Starting application setup ===')

# Try importing the app instance using multiple approaches
def get_flask_app():
    # First try to import directly from app.py
    try:
        logger.info('Trying to import app from app.py module...')
        sys.path.insert(0, os.getcwd())
        import app as app_module
        
        if hasattr(app_module, 'app'):
            logger.info('Found app instance in app.py module')
            return app_module.app
        elif hasattr(app_module, 'create_app'):
            logger.info('Found create_app function in app.py module')
            return app_module.create_app()
    except Exception as e:
        logger.warning(f'Error importing from app.py: {e}')
    
    # If that fails, try importing from app package
    try:
        logger.info('Trying to import app from app package...')
        from app import app as flask_app
        if flask_app is not None:
            logger.info('Found app instance in app package')
            return flask_app
    except Exception as e:
        logger.warning(f'Error importing from app package: {e}')
    
    # As a last resort, import and execute app.py directly
    try:
        logger.info('Trying to execute app.py directly...')
        with open('app.py') as f:
            app_code = f.read()
        globals_dict = {}
        exec(app_code, globals_dict)
        
        if 'app' in globals_dict:
            logger.info('Found app in app.py globals after execution')
            return globals_dict['app']
        elif 'create_app' in globals_dict:
            logger.info('Found create_app in app.py globals after execution')
            return globals_dict['create_app']()
    except Exception as e:
        logger.error(f'Error executing app.py: {e}')
    
    raise ImportError("Could not find Flask app instance by any method")

try:
    flask_app = get_flask_app()
    
    # Add file handler to the Flask logger
    flask_app.logger.addHandler(handler)
    flask_app.logger.setLevel(logging.DEBUG)
    
    # Log startup information
    flask_app.logger.info('=== Starting application on port 8080 ===')
    flask_app.logger.info(f'Log file: {log_filename}')
    flask_app.logger.info(f'Environment: {os.getenv("FLASK_ENV", "development")}')
    
    if __name__ == '__main__':
        flask_app.run(host='0.0.0.0', port=8080, debug=True)
except Exception as e:
    logger.error(f'Failed to start application: {e}', exc_info=True)
    sys.exit(1) 