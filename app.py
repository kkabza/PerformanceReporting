from flask import Flask, render_template
from dotenv import load_dotenv
import os
import sys
import atexit
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from app.routes.home import home_bp

# Load environment variables
load_dotenv()

# Add current directory to path if needed
sys.path.insert(0, os.getcwd())

# Initialize Sentry
SENTRY_DSN = os.getenv('SENTRY_DSN')
ENVIRONMENT = os.getenv('FLASK_ENV', 'development')

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FlaskIntegration()],
        environment=ENVIRONMENT,
        
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        profiles_sample_rate=1.0,
        
        # Enable release tracking for better versioning
        release=os.getenv('APP_VERSION', '0.1.0'),
        
        # Record user information on errors
        send_default_pii=True,
        
        # Configure before_send to filter sensitive information
        before_send=lambda event, hint: event
    )
    print(f"Sentry initialized in {ENVIRONMENT} environment")
else:
    print("Sentry DSN not configured. Error monitoring disabled.")

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')

# Disable CSRF for testing if needed
if ENVIRONMENT == 'development':
    app.config['WTF_CSRF_ENABLED'] = False

# Ensure static files are properly served
app.static_folder = 'app/static'
app.template_folder = 'app/templates'

# Register blueprints
app.register_blueprint(home_bp)

# Enable TDD report enforcement - Never skip build reports
try:
    from app.utils import report_enforcer
    app.config['REPORT_ENFORCER_ENABLED'] = True
    
    # Register cleanup function to generate a report if app exits
    def ensure_report_on_exit():
        report_enforcer.enforce_report_generation()
    
    atexit.register(ensure_report_on_exit)
except ImportError:
    app.config['REPORT_ENFORCER_ENABLED'] = False
    print("WARNING: Report enforcer not available. Build reports may be skipped!")

# Configure Flask error handlers to ensure Sentry captures errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500

def create_app():
    """Factory function to create the Flask application"""
    return app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 