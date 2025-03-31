from flask import Blueprint, render_template, current_app
import os
import sentry_sdk
from app.utils.sentry_utils import capture_message, capture_exception

# Create blueprint
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return render_template('pages/home.html', title="Florida Tax Certificate Sales")

@home_bp.route('/debug-sentry')
def test_sentry():
    """Test endpoint for Sentry integration"""
    sentry_dsn = os.getenv('SENTRY_DSN')
    if not sentry_dsn:
        return "Sentry not configured. Set SENTRY_DSN environment variable to enable error tracking."
    
    # Log a test message
    capture_message("Sentry test message from Florida Tax Certificate Sales app", level="info")
    
    return "Sentry test successful! Check your Sentry dashboard for the test message."

@home_bp.route('/debug-sentry-error')
def trigger_error():
    """Trigger a test error for Sentry"""
    sentry_dsn = os.getenv('SENTRY_DSN')
    if not sentry_dsn:
        return "Sentry not configured. Set SENTRY_DSN environment variable to enable error tracking."
    
    try:
        # Intentionally raise an error
        division_by_zero = 1 / 0
    except Exception as e:
        capture_exception()
        return "Error triggered and captured by Sentry! Check your dashboard." 