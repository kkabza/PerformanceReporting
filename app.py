from flask import Flask, render_template
from dotenv import load_dotenv
import os
from app.routes.home import home_bp

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')

# Register blueprints
app.register_blueprint(home_bp)

def create_app():
    """Factory function to create the Flask application"""
    return app

if __name__ == '__main__':
    app.run(debug=True) 