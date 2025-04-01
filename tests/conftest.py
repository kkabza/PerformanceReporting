import pytest
import os
import threading
import time
import requests
import signal
import atexit
from contextlib import contextmanager
from app import create_app
from flask import Flask
from config.testing import TestingConfig
import logging
import sys
from werkzeug.serving import make_server

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

class FlaskTestServer:
    def __init__(self, app, host='127.0.0.1', port=8080):
        self.app = app
        self.host = host
        self.port = port
        self.server = make_server(host, port, app)
        self.thread = None
        self._stop = threading.Event()
        
    def start(self):
        """Start the server in a separate thread"""
        logger.info(f"Starting Flask test server on {self.host}:{self.port}")
        self.thread = threading.Thread(target=self._run_server)
        self.thread.daemon = True
        self.thread.start()
        
        # Wait for server to start
        self._wait_for_server()
        
    def _run_server(self):
        """Run the server until the stop event is set"""
        with self.app.app_context():
            while not self._stop.is_set():
                self.server.handle_request()
                
    def _wait_for_server(self, timeout=30, check_interval=0.1):
        """Wait for server to be available"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"http://{self.host}:{self.port}/")
                if response.status_code in (200, 302):  # 200 OK or 302 Redirect
                    logger.info("Server is up and running")
                    return True
            except requests.ConnectionError:
                time.sleep(check_interval)
        raise TimeoutError(f"Server did not start within {timeout} seconds")
    
    def stop(self):
        """Stop the server and cleanup resources"""
        logger.info("Stopping Flask test server")
        self._stop.set()
        if self.thread and self.thread.is_alive():
            # Make a final request to trigger handle_request() to process the stop event
            try:
                requests.get(f"http://{self.host}:{self.port}/")
            except requests.ConnectionError:
                pass
            self.thread.join(timeout=5)
        self.server.server_close()
        logger.info("Flask test server stopped")

@pytest.fixture(scope="session")
def app():
    """Create and configure a new app instance for each test session."""
    logger.info("Setting up Flask app fixture")
    
    # Set test environment variables
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['TESTING'] = 'true'
    
    # Create app with testing config
    app = create_app(TestingConfig)
    
    # Update config for testing
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SERVER_NAME": "localhost:8080"
    })
    
    # Create test directories if they don't exist
    os.makedirs(app.config['LOG_DIR'], exist_ok=True)
    os.makedirs(app.config['BUILD_REPORTS_DIR'], exist_ok=True)
    
    yield app
    
    # Cleanup after tests
    try:
        logger.info("Cleaning up test files")
        # Remove test log files
        for file in os.listdir(app.config['LOG_DIR']):
            if file.endswith('.log.txt'):
                try:
                    os.remove(os.path.join(app.config['LOG_DIR'], file))
                except OSError as e:
                    logger.warning(f"Failed to remove log file {file}: {e}")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

@pytest.fixture(scope="session")
def flask_server(app):
    """Start a Flask server for the test session"""
    server = FlaskTestServer(app)
    server.start()
    yield server
    server.stop()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def selenium_config(flask_server):
    """Configure Selenium to work with the Flask server"""
    return {
        "base_url": f"http://{flask_server.host}:{flask_server.port}"
    } 