"""
Base configuration for the Florida Tax Certificate Sale application.
Contains settings common to all environments.
"""
import os
from datetime import timedelta

class BaseConfig:
    """Base configuration class with common settings."""
    
    # Application name and version
    APP_NAME = "Florida Tax Certificate Sale"
    APP_VERSION = os.getenv('APP_VERSION', '0.1.0')
    BUILD_VERSION = os.getenv('BUILD_VERSION', f"BUILD-20250331-{os.getenv('GIT_HASH', 'dev')}")
    
    # Security settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'set-this-in-production')
    WTF_CSRF_ENABLED = True
    
    # File paths
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    STATIC_FOLDER = os.path.join(BASE_DIR, 'app/static')
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'app/templates')
    
    # Database settings - defaults to SQLite for simplicity
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Logging settings
    LOG_DIR = os.path.join(BASE_DIR, 'instance', 'logs')
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s [%(levelname)s] %(module)s: %(message)s'
    LOG_FILE_EXTENSION = '.log.txt'  # Enforced by our logging rules
    
    # Cache configuration
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Session settings
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(BASE_DIR, 'instance', 'sessions')
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Error tracking with Sentry
    SENTRY_DSN = os.getenv('SENTRY_DSN', None)
    
    # Build report settings
    BUILD_REPORTS_DIR = os.path.join(BASE_DIR, 'build_reports')
    
    # Default TDD settings
    REPORT_ENFORCER_ENABLED = True
    
    # API configuration
    API_VERSION = 'v1'
    
    # Feature flags
    FEATURES = {
        'user_registration': True,
        'auction_bidding': True,
        'payment_processing': True,
        'certificate_management': True
    }
    
    @classmethod
    def init_app(cls, app):
        """Initialize the Flask application with this configuration."""
        # Ensure required directories exist
        os.makedirs(cls.LOG_DIR, exist_ok=True)
        os.makedirs(cls.SESSION_FILE_DIR, exist_ok=True)
        os.makedirs(cls.BUILD_REPORTS_DIR, exist_ok=True) 