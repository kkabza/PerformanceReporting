# App package
import os
import sys
import importlib.util

# This tracks whether we're in the process of importing the app
_importing_app = False

def get_app():
    """Helper function to get the Flask app instance without causing circular imports"""
    global _importing_app
    
    # If we're already in the process of importing the app, return None
    if _importing_app:
        import logging
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
            import logging
            logging.getLogger(__name__).error("Could not find Flask app instance in app.py")
            return None
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Error importing app.py: {e}")
        return None
    finally:
        # Reset the importing flag
        _importing_app = False

# Export the app instance
app = get_app() 