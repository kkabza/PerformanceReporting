import pytest
import requests
import time
import os
from flask import url_for

def test_homepage_loads():
    """Test that the homepage loads correctly on port 8080"""
    # Give the server a moment to start up if needed
    time.sleep(1)
    
    # Get port from environment, default to 8080
    port = int(os.environ.get('FLASK_RUN_PORT', 8080))
    
    # The URL to check
    url = f"http://localhost:{port}"
    
    # Try to access the home page
    try:
        response = requests.get(url, timeout=5)
        
        # Verify status code
        assert response.status_code == 200, f"Homepage returned HTTP {response.status_code}"
        
        # Check if the page contains expected content
        assert "Florida Tax Certificate" in response.text, "Homepage doesn't contain expected content"
        
        print(f"✅ Homepage test passed: Successfully loaded homepage on port {port}")
        return True
    except requests.RequestException as e:
        pytest.fail(f"Error accessing homepage: {str(e)}")
    except AssertionError as e:
        pytest.fail(f"Homepage test failed: {str(e)}")

if __name__ == "__main__":
    # Run the test directly when executed as a script
    test_homepage_loads() 