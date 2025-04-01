import pytest
from app import create_app
import os

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

def test_app_creation(app):
    """Test that the app is created successfully."""
    assert app is not None
    assert app.config['TESTING'] is True

def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Performance Reporting' in response.data

def test_sentry_integration(client):
    """Test that Sentry is properly configured."""
    response = client.get('/debug-sentry')
    assert response.status_code == 200
    assert b'Sentry test successful' in response.data 