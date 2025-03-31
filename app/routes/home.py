from flask import Blueprint, render_template

# Create blueprint
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('pages/home.html', title="Florida Tax Certificate Sales") 