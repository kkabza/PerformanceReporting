"""
Utility functions for Sentry integration
"""
import os
import sys
import sentry_sdk
from flask import current_app, request, session
import traceback
from sentry_sdk.integrations.flask import FlaskIntegration

def init_sentry(app):
    """
    Initialize Sentry for the Flask application.
    
    Args:
        app: Flask application instance
    """
    if not os.getenv('SENTRY_DSN'):
        app.logger.warning('SENTRY_DSN not set, skipping Sentry initialization')
        return
        
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[FlaskIntegration()],
        environment=os.getenv('FLASK_ENV', 'development'),
        traces_sample_rate=1.0,
        send_default_pii=True
    )
    app.logger.info('Sentry initialized in %s environment', os.getenv('FLASK_ENV', 'development'))

def set_user_context(user_id=None, username=None, email=None):
    """
    Set Sentry user context for better error tracking.
    
    Args:
        user_id (str, optional): User ID
        username (str, optional): Username
        email (str, optional): User email
    """
    if not os.getenv('SENTRY_DSN'):
        return
        
    user_data = {}
    if user_id:
        user_data['id'] = user_id
    if username:
        user_data['username'] = username
    if email:
        user_data['email'] = email
        
    # Add IP address if available
    if request:
        user_data['ip_address'] = request.remote_addr
        
    sentry_sdk.set_user(user_data)

def set_tag(key, value):
    """
    Set a tag for the current Sentry scope.
    
    Args:
        key (str): Tag key
        value (str): Tag value
    """
    if not os.getenv('SENTRY_DSN'):
        return
        
    sentry_sdk.set_tag(key, value)

def capture_message(message, level="info"):
    """
    Capture a message in Sentry.
    
    Args:
        message (str): Message to capture
        level (str, optional): Message level (debug, info, warning, error)
    """
    if not os.getenv('SENTRY_DSN'):
        return
        
    sentry_sdk.capture_message(message, level=level)

def capture_exception(exc_info=None):
    """
    Capture an exception in Sentry.
    
    Args:
        exc_info (tuple, optional): Exception info as returned by sys.exc_info()
    """
    if not os.getenv('SENTRY_DSN'):
        print("Sentry not configured, exception not captured:", file=sys.stderr)
        traceback.print_exc()
        return
        
    sentry_sdk.capture_exception(exc_info)

def configure_scope(with_request=True, with_session=True):
    """
    Configure the Sentry scope with additional context data.
    
    Args:
        with_request (bool, optional): Include request data
        with_session (bool, optional): Include session data
    """
    if not os.getenv('SENTRY_DSN'):
        return
        
    with sentry_sdk.configure_scope() as scope:
        # Add environment info
        scope.set_tag("environment", os.getenv('FLASK_ENV', 'development'))
        
        # Add application version
        scope.set_tag("version", os.getenv('APP_VERSION', '0.1.0'))
        
        # Add request data if available
        if with_request and request:
            try:
                scope.set_context("request", {
                    "url": request.url,
                    "method": request.method,
                    "headers": dict(request.headers),
                    "params": dict(request.args),
                    "endpoint": request.endpoint
                })
            except:
                pass
                
        # Add session data if available
        if with_session and session:
            try:
                # Filter out sensitive data
                safe_session = {k: v for k, v in session.items() 
                                if k.lower() not in ('password', 'token', 'auth')}
                scope.set_context("session", safe_session)
            except:
                pass 