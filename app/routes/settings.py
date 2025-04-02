from flask import Blueprint, render_template, jsonify, request, Response
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
            return Response(
                json.dumps({'success': False, 'error': 'Invalid JSON in request'}, ensure_ascii=True),
                mimetype='application/json; charset=utf-8',
                status=400
            )
            
        if not data:
            current_app.logger.error("No JSON data in request")
            return Response(
                json.dumps({'success': False, 'error': 'No data provided'}, ensure_ascii=True),
                mimetype='application/json; charset=utf-8',
                status=400
            )
        
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
            return Response(
                json.dumps({'success': False, 'error': 'No Grafana URL provided'}, ensure_ascii=True),
                mimetype='application/json; charset=utf-8',
                status=400
            )
        
        if not api_key:
            return Response(
                json.dumps({'success': False, 'error': 'No Grafana API key provided'}, ensure_ascii=True),
                mimetype='application/json; charset=utf-8',
                status=400
            )
        
        # Format URL correctly
        if url.startswith('http://'):
            url = url[7:]
        elif url.startswith('https://'):
            url = url[8:]
        
        url = url.rstrip('/')
        full_url = f"http://{url}"
        
        current_app.logger.info(f"Testing connection to Grafana at: {full_url}")
        
        # Set up headers with API key
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Test connection by fetching datasources
        endpoint = f"{full_url}/api/datasources"
        current_app.logger.info(f"Testing endpoint: {endpoint}")
        
        response = requests.get(
            endpoint,
            headers=headers,
            timeout=10,
            verify=False  # Disable SSL verification for testing
        )
        
        current_app.logger.info(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            current_app.logger.info("Grafana connection successful")
            return Response(
                json.dumps({'success': True}, ensure_ascii=True),
                mimetype='application/json; charset=utf-8',
                status=200
            )
        elif response.status_code == 401 or response.status_code == 403:
            current_app.logger.error(f"Authentication failed: {response.text}")
            return Response(
                json.dumps({
                    'success': False, 
                    'error': f'Authentication failed: {response.text}'
                }, ensure_ascii=True),
                mimetype='application/json; charset=utf-8',
                status=200  # Return 200 so we can display the error message
            )
        else:
            current_app.logger.error(f"Connection failed with status {response.status_code}: {response.text}")
            return Response(
                json.dumps({
                    'success': False, 
                    'error': f'Connection failed with status {response.status_code}: {response.text}'
                }, ensure_ascii=True),
                mimetype='application/json; charset=utf-8',
                status=200  # Return 200 so we can display the error message
            )
            
    except Exception as e:
        current_app.logger.error(f"Error testing Grafana connection: {str(e)}")
        return Response(
            json.dumps({
                'success': False, 
                'error': f'Error connecting to Grafana: {str(e)}'
            }, ensure_ascii=True),
            mimetype='application/json; charset=utf-8',
            status=500
        )

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
    
    # Begin special debugging for API key issue
    # First, try a raw HTTP call to /api/datasources endpoint as a simple API test
    try:
        current_app.logger.info("DIRECT DEBUG TEST: Testing direct Grafana API connection")
        raw_url = url or os.getenv('GRAFANA_URL')
        raw_key = api_key or os.getenv('GRAFANA_API_TOKEN')
        
        if not raw_url.startswith(('http://', 'https://')):
            raw_url = f"http://{raw_url}"
        
        test_endpoint = f"{raw_url}/api/datasources"
        current_app.logger.info(f"DIRECT DEBUG TEST: Testing endpoint: {test_endpoint}")
        
        test_response = requests.get(
            test_endpoint, 
            headers={
                'Authorization': f'Bearer {raw_key}'
            },
            verify=False,
            timeout=10
        )
        
        current_app.logger.info(f"DIRECT DEBUG TEST: Status code: {test_response.status_code}")
        current_app.logger.info(f"DIRECT DEBUG TEST: Response headers: {dict(test_response.headers)}")
        
        if test_response.status_code == 200:
            current_app.logger.info(f"DIRECT DEBUG TEST: Success! Response: {test_response.text[:500]}")
        else:
            current_app.logger.error(f"DIRECT DEBUG TEST: Failed! Response: {test_response.text[:500]}")
    except Exception as e:
        current_app.logger.error(f"DIRECT DEBUG TEST: Exception: {str(e)}")
    # End special debugging
    
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
    
    # Try different auth methods - sometimes Grafana supports different formats
    auth_methods = [
        {'Authorization': f'Bearer {api_key}'},
        {'Authorization': f'token {api_key}'},
        {'Authorization': api_key},
        {'X-Grafana-Org-Id': '1', 'Authorization': f'Bearer {api_key}'}
    ]
    
    # Track errors for each auth method
    auth_errors = []
    
    for auth_header in auth_methods:
        try:
            current_app.logger.info(f"Trying auth method: {auth_header}")
            
            # Set up headers for API request
            headers = auth_header.copy()
            headers.update({
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            })
            
            # Log the full headers for debugging (without the actual key value)
            debug_headers = headers.copy()
            if 'Authorization' in debug_headers:
                if debug_headers['Authorization'].startswith('Bearer '):
                    debug_headers['Authorization'] = 'Bearer ***MASKED***'
                elif debug_headers['Authorization'].startswith('token '):
                    debug_headers['Authorization'] = 'token ***MASKED***'
                else:
                    debug_headers['Authorization'] = '***MASKED***'
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
            
            # First try the ds/query endpoint (Grafana 8+)
            ds_query_url = f"{full_url}/api/ds/query"
            current_app.logger.info(f"Trying endpoint: {ds_query_url}")
            
            response = requests.post(
                ds_query_url,
                headers=headers,
                json=payload,
                timeout=30,
                verify=verify_ssl
            )
            
            # Log response status
            current_app.logger.info(f"Response status: {response.status_code}")
            
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
            
            # If auth failure, track but try the next method
            if response.status_code == 401 or response.status_code == 403:
                error_text = response.text
                try:
                    error_json = response.json()
                    error_text = json.dumps(error_json)
                except:
                    pass
                auth_errors.append(f"Auth method {auth_header.get('Authorization', 'unknown')[:10]}... failed: {error_text}")
            
        except Exception as e:
            current_app.logger.error(f"Error with auth method {auth_header}: {str(e)}")
            auth_errors.append(f"Auth method exception: {str(e)}")
    
    # If we get here, all auth methods failed
    current_app.logger.error("All authentication methods failed")
    return jsonify({
        'success': False,
        'error': f'Authentication failed with all methods. Details: {"; ".join(auth_errors)}'
    }) 