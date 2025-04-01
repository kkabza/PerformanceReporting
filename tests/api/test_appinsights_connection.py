import pytest
import os
import json
from unittest.mock import patch, MagicMock


class TestAppInsightsConnection:
    """Test the Application Insights connection endpoint"""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, app, client, app_context):
        """Set up and tear down for tests"""
        # Set test environment variables
        os.environ['APP_INSIGHTS_APPLICATION_ID'] = 'test-app-id'
        os.environ['APP_INSIGHTS_API_KEY'] = 'test-api-key'
        
        # Assign fixtures to self
        self.app = app
        self.client = client
        self.app_context = app_context
        
        yield  # This is where the test runs
        
        # Tear down after test
        os.environ.pop('APP_INSIGHTS_APPLICATION_ID', None)
        os.environ.pop('APP_INSIGHTS_API_KEY', None)

    def test_missing_credentials(self):
        """Test the endpoint when credentials are missing"""
        # Remove credentials for this test
        os.environ.pop('APP_INSIGHTS_APPLICATION_ID', None)
        os.environ.pop('APP_INSIGHTS_API_KEY', None)
        
        # Test the endpoint
        response = self.client.post('/settings/api/appinsights/test-connection')
        data = json.loads(response.data)
        
        # Assert response status and content
        assert response.status_code == 400
        assert data['success'] is False
        assert 'Missing Application Insights credentials' in data['error']

    @patch('app.routes.settings.requests.get')
    def test_successful_connection(self, mock_get):
        """Test successful connection to Application Insights"""
        # Mock the requests.get response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'tables': [
                {
                    'rows': [
                        ['row1_data'],
                        ['row2_data']
                    ]
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Test the endpoint
        response = self.client.post('/settings/api/appinsights/test-connection')
        data = json.loads(response.data)
        
        # Assert response status and content
        assert response.status_code == 200
        assert data['success'] is True
        assert 'Successfully connected to Application Insights' in data['message']
        assert data['rows_count'] == 2

    @patch('app.routes.settings.requests.get')
    def test_failed_connection(self, mock_get):
        """Test failed connection to Application Insights"""
        # Mock the requests.get response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = 'Unauthorized'
        mock_get.return_value = mock_response
        
        # Test the endpoint
        response = self.client.post('/settings/api/appinsights/test-connection')
        data = json.loads(response.data)
        
        # Assert response status and content
        assert response.status_code == 400
        assert data['success'] is False
        assert 'Error 401' in data['error']

    @patch('app.routes.settings.requests.get')
    def test_request_exception(self, mock_get):
        """Test handling of request exceptions"""
        # Mock the requests.get to raise an exception
        mock_get.side_effect = Exception("Connection failed")
        
        # Test the endpoint
        response = self.client.post('/settings/api/appinsights/test-connection')
        data = json.loads(response.data)
        
        # Assert response status and content
        assert response.status_code == 400
        assert data['success'] is False
        assert 'Connection error' in data['error']
