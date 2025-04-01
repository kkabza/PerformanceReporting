import requests
import json
import os
from flask import Flask, session
from app import app
from app.routes.auth import login_required
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_grafana_connection():
    """Test the Grafana connection endpoint directly."""
    try:
        # Create a test client
        with app.test_client() as client:
            # Simulate login
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['user_email'] = 'test@example.com'
                sess['logged_in'] = True
                sess['is_authenticated'] = True
            
            # Define test data
            test_data = {
                'url': 'http://10.0.10.16:3000',
                'api_key': 'TKbFkhEnwHiOFnIwVRAI4VNZoIKD2FaM5S1XTpE_En8nJdQ6BXBjXT1JBDjy3dXCAuMYe33zqqqCpMmXK1TLZA=='
            }
            
            # Test the connection endpoint
            logger.info("Testing Grafana connection endpoint...")
            response = client.post(
                '/settings/api/grafana/test-connection',
                data=json.dumps(test_data),
                content_type='application/json'
            )
            
            logger.info(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json
                logger.info(f"Response data: {response_data}")
                return response_data
            else:
                logger.error(f"Error: {response.status_code} - {response.data}")
                return None
    except Exception as e:
        logger.error(f"Error testing Grafana connection: {str(e)}")
        return None

if __name__ == "__main__":
    result = test_grafana_connection()
    print("Test result:", result) 