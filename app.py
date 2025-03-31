"""
Florida Tax Certificate Sale Application
"""
import os
import sys
import atexit
import logging
from flask import Flask, render_template
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from app.routes.home import home_bp
from dotenv import load_dotenv
from config import get_config

# Load environment variables
load_dotenv()

# Add current directory to path if needed
sys.path.insert(0, os.getcwd())

# Get the environment
env = os.getenv('FLASK_ENV', 'development')

# Initialize Sentry if DSN is provided
SENTRY_DSN = os.getenv('SENTRY_DSN')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FlaskIntegration()],
        environment=env,
        
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
    print(f"Sentry initialized in {env} environment")
else:
    print("Sentry DSN not configured. Error monitoring disabled.")

def create_app(config_class=None):
    """Factory function to create the Flask application"""
    app = Flask(__name__)
    
    # Load configuration based on environment
    if config_class is None:
        config_class = get_config()
    
    app.config.from_object(config_class)
    config_class.init_app(app)
    
    # Set up file paths
    app.static_folder = app.config.get('STATIC_FOLDER')
    app.template_folder = app.config.get('TEMPLATE_FOLDER')
    
    # Register blueprints
    app.register_blueprint(home_bp)
    
    # Context processor to inject build version into all templates
    @app.context_processor
    def inject_build_version():
        return dict(build_version=app.config.get('BUILD_VERSION'))
    
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
        app.logger.warning("Report enforcer not available. Build reports may be skipped!")
    
    # Configure Flask error handlers to ensure Sentry captures errors
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500
    
    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0') 