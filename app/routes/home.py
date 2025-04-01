from flask import Blueprint, render_template, current_app, redirect, url_for, session
import os
import sentry_sdk
from app.utils.sentry_utils import capture_message, capture_exception
from app.routes.auth import login_required

# Create blueprint
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    """Redirect to login if not authenticated, otherwise show dashboard."""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return redirect(url_for('home.dashboard'))

@home_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page route."""
    return render_template('pages/dashboard.html', title="Dashboard")

@home_bp.route('/debug-sentry')
def test_sentry():
    """Test endpoint for Sentry integration"""
    sentry_dsn = os.getenv('SENTRY_DSN')
    if not sentry_dsn:
        return "Sentry not configured. Set SENTRY_DSN environment variable to enable error tracking."
    
    # Log a test message
    capture_message("Sentry test message from Performance Reporting app", level="info")
    
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