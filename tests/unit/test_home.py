"""
Unit tests for home routes
"""
import unittest
from app import app

class TestHomeRoutes(unittest.TestCase):
    """Test suite for home routes"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_route(self):
        """Test the home route returns 200 status code"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Florida Tax Certificate', response.data)
    
    def test_home_title(self):
        """Test the home page has the correct title"""
        response = self.app.get('/')
        self.assertIn(b'<title>Florida Tax Certificate Sales</title>', response.data)

if __name__ == '__main__':
    unittest.main() 