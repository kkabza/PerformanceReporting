"""
Testing configuration for the Performance Reporting application.
This configuration is optimized for CI/CD use.
"""
import os
import tempfile
from config.base import BaseConfig

class TestingConfig(BaseConfig):
    """Testing environment specific configuration."""
    
    # Enable testing mode
    TESTING = True
    DEBUG = False
    
    # Disable CSRF in tests for easier form submission testing
    WTF_CSRF_ENABLED = False
    
    # Use in-memory database for faster tests
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///:memory:')
    
    # Turn off SQL query logging during tests for cleaner output
    SQLALCHEMY_ECHO = False
    
    # Disable extensions that make testing harder
    CACHE_TYPE = 'NullCache'
    
    # Logs and reports directories (use temp directory to avoid cluttering test environment)
    LOG_DIR = os.path.join(tempfile.gettempdir(), 'performance_reporting_test_logs')
    BUILD_REPORTS_DIR = os.path.join(tempfile.gettempdir(), 'performance_reporting_test_reports')
    
    # Session and cache
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(tempfile.gettempdir(), 'performance_reporting_test_sessions')
    
    # Disable Sentry in tests
    SENTRY_DSN = None
    
    # Test-specific feature flags
    FEATURES = {
        **BaseConfig.FEATURES,
        'debug_toolbar': False,
        'mock_payment': True,
        'demo_mode': True
    }
    
    # Mock third-party services for testing
    API_ENDPOINTS = {
        'payment_gateway': 'mock://',
        'certificate_authority': 'mock://',
        'data_service': 'mock://'
    }
    
    @classmethod
    def init_app(cls, app):
        """Initialize the Flask application with testing-specific settings."""
        BaseConfig.init_app(app)
        
        # Set up test-specific logging
        import logging
        app.logger.setLevel(logging.ERROR)
        
        # Create clean test directories
        for test_dir in [cls.LOG_DIR, cls.BUILD_REPORTS_DIR, cls.SESSION_FILE_DIR]:
            if not os.path.exists(test_dir):
                os.makedirs(test_dir)
                
        # Configure test client
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        app.config['SERVER_NAME'] = 'localhost.test' 