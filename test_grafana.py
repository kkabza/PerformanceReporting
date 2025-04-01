#!/usr/bin/env python3
"""
Test script for Grafana connection
This script verifies the connection to Grafana using environment variables
"""

import os
import json
import requests
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_grafana_connection():
    """Test connection to Grafana API"""
    url = os.getenv('GRAFANA_URL')
    api_key = os.getenv('GRAFANA_API_TOKEN')
    
    if not url:
        print("ERROR: GRAFANA_URL not set in .env file")
        return False
        
    if not api_key:
        print("ERROR: GRAFANA_API_TOKEN not set in .env file")
        return False
    
    print(f"Testing connection to Grafana at: {url}")
    
    # Add trailing slash if missing
    if not url.endswith('/'):
        url += '/'
        
    # Set headers with proper encoding
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json, text/plain',
        'Accept-Charset': 'utf-8'
    }
    
    try:
        # Test health endpoint
        health_url = f"{url}api/health"
        print(f"Checking health at: {health_url}")
        
        response = requests.get(health_url, headers=headers, timeout=10)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            response.encoding = 'utf-8'  # Force UTF-8 encoding
            print("Health check successful!")
            print(f"Response: {response.text}")
            
            # Try to get version info
            print("\nChecking Grafana version...")
            version_url = f"{url}api/frontend/settings"
            version_response = requests.get(version_url, headers=headers, timeout=10)
            
            if version_response.status_code == 200:
                version_response.encoding = 'utf-8'  # Force UTF-8 encoding
                version_data = version_response.json()
                if 'buildInfo' in version_data:
                    version = version_data['buildInfo'].get('version', 'Unknown')
                    print(f"Grafana version: {version}")
                else:
                    print("Version information not available in response")
            else:
                print(f"Failed to get version info: {version_response.status_code}")
            
            # Try to get datasources
            print("\nChecking Grafana datasources...")
            datasources_url = f"{url}api/datasources"
            datasources_response = requests.get(datasources_url, headers=headers, timeout=10)
            
            if datasources_response.status_code == 200:
                datasources_response.encoding = 'utf-8'  # Force UTF-8 encoding
                datasources = datasources_response.json()
                print(f"Found {len(datasources)} datasources:")
                
                for ds in datasources:
                    print(f"  - {ds.get('name', 'Unnamed')} (Type: {ds.get('type', 'Unknown')})")
            else:
                print(f"Failed to get datasources: {datasources_response.status_code}")
            
            print("\nTest completed successfully!")
            return True
        else:
            print(f"Health check failed with status: {response.status_code}")
            try:
                print(f"Response: {response.text}")
            except:
                print("Could not decode response")
            return False
            
    except Exception as e:
        print(f"Error testing Grafana connection: {str(e)}")
        return False

if __name__ == "__main__":
    print("Grafana Connection Test")
    print("======================")
    success = test_grafana_connection()
    sys.exit(0 if success else 1) 