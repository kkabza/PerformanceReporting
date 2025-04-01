"""
Production configuration for the Performance Reporting application.
This configuration is optimized for security and performance.
"""
import os
from config.base import BaseConfig

class ProductionConfig(BaseConfig):
    """Production environment specific configuration."""
    
    # Disable debug features in production
    DEBUG = False
    TESTING = False
    
    # Enforce security measures
    WTF_CSRF_ENABLED = True
    
    # Set strict content security policy
    CONTENT_SECURITY_POLICY = {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' cdn.tailwindcss.com cdnjs.cloudflare.com",
        'style-src': "'self' 'unsafe-inline' cdn.tailwindcss.com cdnjs.cloudflare.com",
        'img-src': "'self' data:",
        'font-src': "'self' cdnjs.cloudflare.com",
        'connect-src': "'self'"
    }
    
    # Configure logging for production
    LOG_LEVEL = 'ERROR'
    
    # Use proper database in production
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # Disable SQL query logging for performance
    SQLALCHEMY_ECHO = False
    
    # Production cache settings
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = os.getenv('REDIS_URL')
    CACHE_DEFAULT_TIMEOUT = 600
    
    # Configure session for production
    SESSION_TYPE = 'redis'
    SESSION_REDIS = os.getenv('REDIS_URL')
    SESSION_USE_SIGNER = True
    SESSION_PERMANENT = True
    
    # Ensure Sentry is configured
    SENTRY_DSN = os.getenv('SENTRY_DSN')
    
    # Disable development features
    FEATURES = {
        **BaseConfig.FEATURES,
        'debug_toolbar': False,
        'mock_payment': False,
        'demo_mode': False
    }
    
    # SSL settings
    PREFERRED_URL_SCHEME = 'https'
    
    @classmethod
    def init_app(cls, app):
        """Initialize the Flask application with production-specific settings."""
        BaseConfig.init_app(app)
        
        # Enhanced security headers
        @app.after_request
        def add_security_headers(response):
            # Enable HTTP Strict Transport Security
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            # Prevent MIME type sniffing
            response.headers['X-Content-Type-Options'] = 'nosniff'
            # Enable Cross-site scripting filter in browser
            response.headers['X-XSS-Protection'] = '1; mode=block'
            # Prevent embedding in frames (clickjacking protection)
            response.headers['X-Frame-Options'] = 'SAMEORIGIN'
            # Set Content Security Policy
            csp_string = '; '.join(f"{key} {value}" for key, value in cls.CONTENT_SECURITY_POLICY.items())
            response.headers['Content-Security-Policy'] = csp_string
            return response
            
        # Configure production logging
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Create secure file logger
        if not os.path.exists(cls.LOG_DIR):
            os.makedirs(cls.LOG_DIR)
            
        file_handler = RotatingFileHandler(
            os.path.join(cls.LOG_DIR, f'app_production{cls.LOG_FILE_EXTENSION}'),
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        
        file_handler.setFormatter(logging.Formatter(cls.LOG_FORMAT))
        file_handler.setLevel(logging.ERROR)
        
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.ERROR)
        
        # Validate critical configuration
        assert cls.SECRET_KEY != 'set-this-in-production', 'Production SECRET_KEY not set!'
        assert cls.SENTRY_DSN is not None, 'Sentry DSN not configured for production!'
        assert cls.SQLALCHEMY_DATABASE_URI is not None, 'Production database URL not set!' 