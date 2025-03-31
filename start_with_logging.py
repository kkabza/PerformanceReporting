#!/usr/bin/env python3
"""
Script to start the Flask application with immediate logging and Sentry error reporting
"""
import os
import sys
import logging
import datetime
import traceback
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Initialize Sentry immediately, before any other imports
try:
    import sentry_sdk
    
    # Get Sentry DSN from environment
    SENTRY_DSN = os.getenv('SENTRY_DSN')
    
    if SENTRY_DSN:
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            # A higher sample rate means potentially more events will be captured
            traces_sample_rate=1.0,
            # Send all errors, even in development
            environment=os.getenv('FLASK_ENV', 'development'),
            # Enable performance monitoring 
            profiles_sample_rate=1.0,
            # Release tracking
            release=os.getenv('BUILD_VERSION', 'BUILD-DEVELOPMENT'),
            # Enable PII if you need user context
            send_default_pii=True,
            # Make sure we capture everything, even early failures
            auto_enabling_integrations=True,
            debug=True
        )
        print(f"Sentry initialized for early error capture")
    else:
        print("WARNING: Sentry DSN not configured. Error monitoring to Sentry is disabled.")
except ImportError:
    print("WARNING: Sentry SDK not installed. Error monitoring to Sentry is disabled.")
    SENTRY_DSN = None

# Create the instance/logs directory if it doesn't exist
instance_dir = Path('instance')
logs_dir = instance_dir / 'logs'
os.makedirs(logs_dir, exist_ok=True)

# Set up logging immediately
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

logger = logging.getLogger('startup')
logger.info('=============================================')
logger.info('Starting application initialization')
logger.info(f'Log file created at: {log_file}')
logger.info(f'Sentry monitoring enabled: {SENTRY_DSN is not None}')

# Function to capture and report errors to both log and Sentry
def report_error(error_msg, exc_info=None):
    """Report an error to both log file and Sentry"""
    # Log to file
    logger.error(error_msg, exc_info=exc_info)
    
    # Also send to Sentry if available
    if SENTRY_DSN:
        with sentry_sdk.push_scope() as scope:
            scope.set_tag("startup_phase", "application_init")
            scope.set_extra("log_file", str(log_file))
            sentry_sdk.capture_exception()
            logger.info("Error reported to Sentry")

try:
    # Import the Flask app
    logger.info('Attempting to import the Flask application')
    
    # Try to import app from root module
    try:
        from app.py import app
        logger.info('Successfully imported the Flask application from app.py')
    except ImportError:
        logger.info('Could not import app directly, trying with factory pattern')
        # Try alternate import patterns
        try:
            from app import create_app
            app = create_app()
            logger.info('Successfully created Flask application using factory pattern')
        except ImportError:
            # Try importing from the app.py file
            try:
                import app as app_module
                app = app_module.app
                logger.info('Successfully imported Flask application from app module')
            except (ImportError, AttributeError):
                # One last attempt - try to import from the app package
                from app import app
                logger.info('Successfully imported Flask application from app package')
    
    # Run the app
    logger.info('Starting the Flask application server')
    app.run(host='0.0.0.0', debug=True)
    
except Exception as e:
    error_message = f'Error starting the application: {str(e)}'
    error_details = traceback.format_exc()
    
    # Report the error to both log and Sentry
    report_error(error_message, exc_info=True)
    logger.error(f'Detailed error information:\n{error_details}')
    
    # Check common configuration issues
    logger.info('Checking for common configuration issues')
    
    # Check if app.py exists
    if not os.path.exists('app.py'):
        logger.error('app.py file not found in the current directory')
    else:
        # If app.py exists, let's peek at its contents
        with open('app.py', 'r') as f:
            app_content = f.read()
            logger.info(f'app.py content preview (first 500 chars):\n{app_content[:500]}...')
    
    # Check app directory structure
    if os.path.exists('app') and os.path.isdir('app'):
        logger.info('app/ directory exists, checking contents:')
        app_files = os.listdir('app')
        logger.info(f'Files in app/: {app_files}')
        
        # Check __init__.py
        if os.path.exists('app/__init__.py'):
            with open('app/__init__.py', 'r') as f:
                init_content = f.read()
                logger.info(f'app/__init__.py content:\n{init_content}')
    
    # Check environment variables
    env_file = '.env'
    if os.path.exists(env_file):
        logger.info(f'Found environment file: {env_file}')
        with open(env_file, 'r') as f:
            env_content = f.read()
            logger.info(f'Environment file contents:\n{env_content}')
    else:
        logger.error(f'Environment file not found: {env_file}')
    
    # Print instructions for fixing
    logger.info('Possible solutions:')
    logger.info('1. Ensure FLASK_APP is correctly set in your .env file')
    logger.info('2. Check that app.py contains a valid Flask application')
    logger.info('3. Verify all required dependencies are installed')
    logger.info('4. Check if app/__init__.py properly exports the Flask app')
    
    # Exit with error code
    sys.exit(1)

logger.info('Application exited normally') 