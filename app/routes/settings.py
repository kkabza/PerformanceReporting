from flask import Blueprint, render_template, jsonify, request, Response, current_app
from app.routes.auth import login_required
import requests
import os
import time
import json

# Create blueprint
settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/general')
@login_required
def general():
    """General settings page route."""
    return render_template('pages/settings/general.html')

@settings_bp.route('/preferences')
def preferences():
    return render_template('pages/settings/preferences.html')

@settings_bp.route('/grafana/test-connection', methods=['POST'])
@settings_bp.route('/api/grafana/test-connection', methods=['POST'])
def test_grafana_connection():
    """Test the connection to Grafana."""
    try:
        current_app.logger.info(f"Grafana test connection requested")
        
        # Get data from request
        try:
            data = request.get_json()
            current_app.logger.info(f"Request JSON data: {data}")
        except Exception as e:
            current_app.logger.error(f"Failed to parse JSON: {str(e)}")
            return jsonify({
                'success': False, 
                'error': 'Invalid JSON in request'
            })
            
        if not data:
            current_app.logger.error("No JSON data in request")
            return jsonify({
                'success': False, 
                'error': 'No data provided'
            })
        
        # Get URL and API key from request or environment variables
        url = data.get('url')
        api_key = data.get('api_key')
        
        if not url:
            url = os.getenv('GRAFANA_URL')
            current_app.logger.info(f"No URL provided, using environment variable: {url}")
        
        if not api_key:
            api_key = os.getenv('GRAFANA_API_TOKEN')
            current_app.logger.info(f"No API key provided, using environment variable (length: {len(api_key) if api_key else 0})")
        
        if not url:
            return jsonify({
                'success': False, 
                'error': 'No Grafana URL provided'
            })
        
        if not api_key:
            return jsonify({
                'success': False, 
                'error': 'No Grafana API key provided'
            })
        
        # Format URL correctly
        if url.startswith('http://'):
            url = url[7:]
            protocol = 'http'
        elif url.startswith('https://'):
            url = url[8:]
            protocol = 'https'
        else:
            protocol = 'http'  # Default to HTTP
            
        url = url.rstrip('/')
        full_url = f"{protocol}://{url}"
        
        current_app.logger.info(f"Testing connection to Grafana at: {full_url}")
        
        # Set up headers with API key
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Test connection by fetching datasources - using a simple health check is more reliable
        endpoint = f"{full_url}/api/health"
        current_app.logger.info(f"Testing endpoint: {endpoint}")
        
        response = requests.get(
            endpoint,
            headers=headers,
            timeout=10,
            verify=False  # Disable SSL verification for testing
        )
        
        current_app.logger.info(f"Response status: {response.status_code}")
        current_app.logger.info(f"Response content type: {response.headers.get('Content-Type', 'unknown')}")
        
        # Check if we received HTML instead of JSON (common error case)
        if response.headers.get('Content-Type', '').startswith('text/html'):
            current_app.logger.error("Received HTML response instead of JSON")
            # Include a snippet of the response to help diagnose the issue
            snippet = response.text[:200] + '...' if len(response.text) > 200 else response.text
            return jsonify({
                'success': False,
                'error': 'Server returned HTML instead of JSON. This usually means a redirect to login page or incorrect URL.',
                'response_preview': snippet
            })
            
        # Try to parse response as JSON, but handle non-JSON responses gracefully
        try:
            if response.status_code == 200:
                result = response.json()
                current_app.logger.info("Grafana connection successful")
                return jsonify({
                    'success': True,
                    'version': result.get('version', 'unknown')
                })
            elif response.status_code == 401 or response.status_code == 403:
                current_app.logger.error(f"Authentication failed: {response.text}")
                return jsonify({
                    'success': False, 
                    'error': f'Authentication failed: {response.text}'
                })
            else:
                current_app.logger.error(f"Connection failed with status {response.status_code}: {response.text}")
                return jsonify({
                    'success': False, 
                    'error': f'Connection failed with status {response.status_code}: {response.text}'
                })
        except ValueError as e:
            # Handle non-JSON responses
            current_app.logger.error(f"Invalid response from server: {str(e)}")
            # Include a snippet of the response to help diagnose the issue
            snippet = response.text[:200] + '...' if len(response.text) > 200 else response.text
            return jsonify({
                'success': False,
                'error': f'Response was not valid JSON: {str(e)}',
                'response_preview': snippet
            })
            
    except requests.exceptions.RequestException as e:
        # Handle network errors
        current_app.logger.error(f"Request exception: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'Error connecting to Grafana: {str(e)}'
        })
    except Exception as e:
        current_app.logger.error(f"Error testing Grafana connection: {str(e)}")
        return jsonify({
            'success': False, 
            'error': f'Error connecting to Grafana: {str(e)}'
        })

@settings_bp.route('/grafana/test-query', methods=['POST'])
@settings_bp.route('/api/grafana/test-query', methods=['POST'])
@login_required
def test_grafana_query():
    """
    Test Grafana API query.
    """
    current_app.logger.info("Starting Grafana test query")
    data = request.get_json()
    url = data.get('url')
    api_key = data.get('api_key')
    query = data.get('query')
    
    current_app.logger.info(f"Received query: {query}")
    current_app.logger.info(f"URL: {url}")
    current_app.logger.info(f"API key length: {len(api_key) if api_key else 0}")
    if api_key:
        current_app.logger.info(f"API key prefix: {api_key[:5]}...")
    
    # If URL or API key is not provided in the request, use environment variables
    if not url or not url.strip():
        url = os.getenv('GRAFANA_URL')
        current_app.logger.info("Using Grafana URL from environment variables")
    
    if not api_key or not api_key.strip():
        api_key = os.getenv('GRAFANA_API_TOKEN')
        current_app.logger.info("Using Grafana API key from environment variables")
    
    # Check for required parameters
    if not url or not url.strip():
        current_app.logger.error("No Grafana URL provided")
        return jsonify({'success': False, 'error': 'Grafana URL is required'})
    
    if not api_key or not api_key.strip():
        current_app.logger.error("No Grafana API key provided")
        return jsonify({'success': False, 'error': 'Grafana API key is required'})
    
    if not query or not query.strip():
        current_app.logger.error("No query provided")
        return jsonify({'success': False, 'error': 'Query is required'})
    
    # Process the URL to ensure proper format
    # First, strip any existing protocol
    if url.startswith('http://'):
        url = url[7:]
        protocol = 'http'
    elif url.startswith('https://'):
        url = url[8:]
        protocol = 'https'
    else:
        # Default to HTTP for local development (more likely to work without certificates)
        protocol = 'http'
    
    # Ensure URL doesn't end with a slash
    url = url.rstrip('/')
    
    # Build the full URL with protocol
    full_url = f"{protocol}://{url}"
    current_app.logger.info(f"Using Grafana URL: {full_url}")
    
    # Try the query with authorization header
    try:
        # Set up headers for API request
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Log the headers for debugging (without the actual key value)
        debug_headers = headers.copy()
        if 'Authorization' in debug_headers:
            debug_headers['Authorization'] = 'Bearer ***MASKED***'
        current_app.logger.info(f"Request headers: {debug_headers}")
        
        # Execute the query through the Grafana API
        current_time = int(time.time())
        one_hour_ago = current_time - 3600
        
        # Simplified payload structure matching expected Grafana API format
        payload = {
            'queries': [
                {
                    'refId': 'A',
                    'datasourceId': 1,  # Default Prometheus datasource
                    'expr': query,
                    'instant': True
                }
            ],
            'from': str(one_hour_ago * 1000),
            'to': str(current_time * 1000)
        }
        
        current_app.logger.info(f"Request payload: {json.dumps(payload)}")
        
        # Disable SSL verification for development
        verify_ssl = False
        current_app.logger.info(f"SSL verification: disabled for testing")
        
        # Try the Grafana API endpoint
        ds_query_url = f"{full_url}/api/ds/query"
        current_app.logger.info(f"Trying endpoint: {ds_query_url}")
        
        response = requests.post(
            ds_query_url,
            headers=headers,
            json=payload,
            timeout=30,
            verify=verify_ssl
        )
        
        # Log response info
        current_app.logger.info(f"Response status: {response.status_code}")
        current_app.logger.info(f"Response content type: {response.headers.get('Content-Type', 'unknown')}")
        
        # Check if we received HTML instead of JSON (common error case)
        if response.headers.get('Content-Type', '').startswith('text/html'):
            current_app.logger.error("Received HTML response instead of JSON")
            # Include a snippet of the response to help diagnose the issue
            snippet = response.text[:500] + '...' if len(response.text) > 500 else response.text
            return jsonify({
                'success': False,
                'error': 'Server returned HTML instead of JSON. This usually means a redirect to login page or incorrect URL.',
                'html_response': snippet
            })
        
        # Try to parse the response as JSON
        try:
            # If success, return the result
            if response.status_code == 200:
                response.encoding = 'utf-8'
                result_data = response.json()
                current_app.logger.info(f"Response data: {json.dumps(result_data)[:500]}...")
                
                # Return success with results
                return jsonify({
                    'success': True,
                    'results': result_data
                })
            
            # Handle auth failures
            if response.status_code == 401 or response.status_code == 403:
                error_text = response.text
                try:
                    error_json = response.json()
                    error_text = json.dumps(error_json)
                except:
                    pass
                
                current_app.logger.error(f"Authentication failed: {error_text}")
                return jsonify({
                    'success': False,
                    'error': f'Authentication failed: {error_text}'
                })
            
            # Handle other errors
            error_text = response.text[:500] if response.text else f"HTTP {response.status_code}"
            current_app.logger.error(f"Query failed: {error_text}")
            return jsonify({
                'success': False,
                'error': f'Query failed: {error_text}'
            })
            
        except ValueError as e:
            # Handle non-JSON responses
            current_app.logger.error(f"Failed to parse Grafana response: {str(e)}")
            current_app.logger.error(f"Response content: {response.text[:500]}")
            
            # Return specific error for invalid JSON
            return jsonify({
                'success': False,
                'error': f'Unexpected token \'{str(e)}\', "{response.text[:20]}..." is not valid JSON',
                'html_response': response.text[:500]
            })
        
    except requests.exceptions.SSLError as e:
        current_app.logger.error(f"SSL Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'SSL certificate validation failed. Your Grafana server may be using a self-signed certificate.'
        })
    except requests.exceptions.ConnectionError as e:
        current_app.logger.error(f"Grafana connection error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Could not connect to Grafana server. Please check the URL and ensure the server is running. Error: {str(e)}'
        })
    except requests.exceptions.Timeout:
        current_app.logger.error("Request timed out")
        return jsonify({
            'success': False,
            'error': 'Query timed out. The query may be too complex or the server is busy.'
        })
    except Exception as e:
        # Generic error handler for any issues
        current_app.logger.error(f"Error executing Grafana query: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'An error occurred with the Grafana query: {str(e)}'
        }) 