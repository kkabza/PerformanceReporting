from flask import Blueprint, render_template
from app.routes.auth import login_required

# Create blueprint
settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/general')
@login_required
def general():
    """General settings page route."""
    return render_template('pages/settings/general.html')

@settings_bp.route('/preferences')
def preferences():
    return render_template('pages/settings/preferences.html') 