# App package
import os
import sys
import importlib.util
from flask import Flask
from flask_assets import Environment, Bundle
from app.routes.home import home_bp
from app.routes.auth import auth_bp
from app.routes.settings import settings_bp
import logging
from app.utils.sentry_utils import init_sentry

# This tracks whether we're in the process of importing the app
_importing_app = False

def get_app():
    """Helper function to get the Flask app instance without causing circular imports"""
    global _importing_app
    
    # If we're already in the process of importing the app, return None
    if _importing_app:
        logging.getLogger(__name__).warning(
            "Circular import detected in app/__init__.py. Returning None for app."
        )
        return None
    
    # Mark that we're importing the app
    _importing_app = True
    
    try:
        # Try to import app.py dynamically to avoid circular imports
        spec = importlib.util.spec_from_file_location("app_module", os.path.join(os.path.dirname(os.path.dirname(__file__)), "app.py"))
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)
        
        # Get the app instance
        if hasattr(app_module, "app"):
            return app_module.app
        elif hasattr(app_module, "create_app"):
            return app_module.create_app()
        else:
            logging.getLogger(__name__).error("Could not find Flask app instance in app.py")
            return None
    except Exception as e:
        logging.getLogger(__name__).error(f"Error importing app.py: {e}")
        return None
    finally:
        # Reset the importing flag
        _importing_app = False

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(settings_bp)
    
    # ... existing code ...

# Export the app instance
app = get_app() 