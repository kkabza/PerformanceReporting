"""
Development configuration for the Florida Tax Certificate Sale application.
This configuration is optimized for local development.
"""
import os
from config.base import BaseConfig

class DevelopmentConfig(BaseConfig):
    """Development environment specific configuration."""
    
    # Enable development mode
    DEBUG = True
    TESTING = False
    
    # Disable CSRF for easier API testing during development
    WTF_CSRF_ENABLED = False
    
    # More verbose logging
    LOG_LEVEL = 'DEBUG'
    
    # SQLite database for development
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DEV_DATABASE_URL', 
        f"sqlite:///{os.path.join(BaseConfig.BASE_DIR, 'instance', 'dev.db')}"
    )
    
    # Enable SQL query logging
    SQLALCHEMY_ECHO = True
    
    # Set shorter cache timeout for development
    CACHE_DEFAULT_TIMEOUT = 60
    
    # Development-specific feature flags
    FEATURES = {
        **BaseConfig.FEATURES,
        'debug_toolbar': True,
        'mock_payment': True,
        'demo_mode': True
    }
    
    # Flask-DebugToolbar settings
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    
    @classmethod
    def init_app(cls, app):
        """Initialize the Flask application with development-specific settings."""
        BaseConfig.init_app(app)
        
        # Print a warning that we're in development mode
        app.logger.warning('Running in development mode. Do not use in production!')
        
        # Register development-specific extensions
        try:
            from flask_debugtoolbar import DebugToolbarExtension
            toolbar = DebugToolbarExtension()
            toolbar.init_app(app)
        except ImportError:
            app.logger.warning('Flask-DebugToolbar not installed, skipping.')
            
        # Enable Flask's debug mode
        app.debug = True 