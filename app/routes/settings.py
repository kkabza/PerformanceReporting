from flask import Blueprint, render_template, jsonify, request, current_app, Response
from app.routes.auth import login_required
import requests
import os
import json
import uuid
import time
import datetime

# Create blueprint
settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/general')
@login_required
def general():
    """General settings page route."""
    # Get App Insights credentials for display in the template
    app_insights_url = os.getenv('AZURE_APP_INSIGHTS_URL', '')
    app_insights_api_key = os.getenv('AZURE_APP_INSIGHTS_API_KEY', '')
    # Mask the API key for security
    app_insights_api_key_masked = "•" * len(app_insights_api_key) if app_insights_api_key else ''
    
    # Get Grafana credentials from environment
    grafana_url = os.getenv('GRAFANA_URL', '')
    grafana_api_key = os.getenv('GRAFANA_API_TOKEN', '')
    # Mask the API key for security
    grafana_api_key_masked = "•" * len(grafana_api_key) if grafana_api_key else ''
    
    return render_template('pages/settings/general.html', 
                           app_insights_url=app_insights_url,
                           app_insights_api_key_masked=app_insights_api_key_masked,
                           grafana_url=grafana_url,
                           grafana_api_key_masked=grafana_api_key_masked)

@settings_bp.route('/preferences')
def preferences():
    return render_template('pages/settings/preferences.html')

@settings_bp.route('/api/appinsights/test-connection', methods=['POST'])
@login_required
def test_appinsights_connection():
    """Test connection to Application Insights using direct API approach."""
    # Get App Insights credentials from environment
    app_id = os.getenv('APP_INSIGHTS_APPLICATION_ID')
    api_key = os.getenv('APP_INSIGHTS_API_KEY')
    
    # Log environment variable values for debugging (with masking for security)
    current_app.logger.info(f"App Insights test connection requested")
    current_app.logger.info(f"APP_INSIGHTS_APPLICATION_ID: {app_id[:4]}... (length: {len(app_id) if app_id else 0})")
    current_app.logger.info(f"APP_INSIGHTS_API_KEY: {'*' * 8}... (length: {len(api_key) if api_key else 0})")
    
    # Check if credentials are available
    if not app_id or not api_key:
        error_msg = 'Missing Application Insights credentials. Check your environment variables.'
        current_app.logger.error(error_msg)
        return jsonify({
            'success': False, 
            'error': error_msg
        }), 400

    # Debug output to help with troubleshooting
    debug_info = {
        'app_id': app_id[:4] + '...' if app_id and len(app_id) > 4 else 'Not set',
        'api_key_length': len(api_key) if api_key else 0,
        'env_vars': {k: v[:4] + '...' if v and len(v) > 4 else v for k, v in os.environ.items() if 'APP_INSIGHTS' in k or 'AZURE' in k}
    }

    try:
        # Define a simple query to get recent traces
        query = "traces | top 5 by timestamp desc"
        
        # Build the URL for the query API
        url = f"https://api.applicationinsights.io/v1/apps/{app_id}/query"
        current_app.logger.info(f"Making App Insights API request to URL: {url}")
        
        # Set up headers with the API key
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        
        # Set query parameters
        params = {
            "query": query
        }
        
        current_app.logger.info(f"Making App Insights API request with query: {query}")
        
        # Send the request
        response = requests.get(url, headers=headers, params=params, timeout=10)
        current_app.logger.info(f"App Insights API response status: {response.status_code}")
        
        # Check response status
        if response.status_code == 200:
            try:
                data = response.json()
                current_app.logger.info("Successfully parsed JSON response")
                
                # Format the results for display
                formatted_rows = []
                column_names = []
                
                if 'tables' in data and len(data['tables']) > 0:
                    # Get column information
                    if 'columns' in data['tables'][0]:
                        column_names = [col['name'] for col in data['tables'][0]['columns']]
                        
                    # Format rows with column names
                    if 'rows' in data['tables'][0]:
                        for row in data['tables'][0]['rows']:
                            # Create dict with column names as keys
                            row_dict = {}
                            for i, col_name in enumerate(column_names):
                                # Handle index errors gracefully
                                if i < len(row):
                                    row_dict[col_name] = row[i]
                                else:
                                    row_dict[col_name] = None
                            formatted_rows.append(row_dict)
                        current_app.logger.info(f"Found {len(formatted_rows)} rows in response")
                    else:
                        current_app.logger.warning("No rows found in response")
                else:
                    current_app.logger.warning("No tables found in response")
                
                # Add metadata for better display
                metadata = {
                    'query_executed_at': datetime.datetime.now().isoformat(),
                    'column_names': column_names,
                    'total_records': len(formatted_rows)
                }
                
                return jsonify({
                    'success': True,
                    'message': 'Successfully connected to Application Insights',
                    'query': query,
                    'rows_count': len(formatted_rows),
                    'sample_data': formatted_rows[:5] if formatted_rows else [],
                    'metadata': metadata
                })
            except json.JSONDecodeError as je:
                # If we can't parse the JSON, return the raw content for debugging
                error_msg = f'Invalid JSON response: {str(je)}'
                current_app.logger.error(error_msg)
                current_app.logger.error(f"Raw response: {response.text[:500]}")
                return jsonify({
                    'success': False,
                    'error': error_msg,
                    'raw_response': response.text[:500],  # Limit to first 500 chars
                    'debug_info': debug_info
                }), 400
        else:
            # Try to interpret the response content
            try:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', str(error_data))
            except:
                error_message = response.text[:500] if response.text else f"Status code: {response.status_code}"
            
            error_msg = f'Error {response.status_code}: {error_message}'
            current_app.logger.error(error_msg)
            current_app.logger.error(f"Raw response: {response.text[:500]}")
            
            return jsonify({
                'success': False, 
                'error': error_msg,
                'debug_info': debug_info
            }), 400

    except requests.exceptions.RequestException as e:
        error_msg = f'Connection error: {str(e)}'
        current_app.logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg,
            'debug_info': debug_info
        }), 400

@settings_bp.route('/api/grafana/test-connection', methods=['POST'])
def test_grafana_connection():
    """Test the connection to Grafana."""
    try:
        data = request.get_json()
        if not data:
            current_app.logger.error("No JSON data in request")
            return Response(
                json.dumps({'success': False, 'error': 'No data provided'}, ensure_ascii=False),
                mimetype='application/json; charset=utf-8',
                status=400
            )

        # Get URL and API key from request or environment variables
        url = data.get('url')
        api_key = data.get('api_key')
        
        if not url:
            url = current_app.config.get('GRAFANA_URL')
            current_app.logger.info(f"No URL provided, using environment variable: {url}")
        
        if not api_key:
            api_key = current_app.config.get('GRAFANA_API_TOKEN')
            current_app.logger.info("No API key provided, using environment variable")
        
        if not url:
            current_app.logger.error("No Grafana URL provided in request or environment")
            return Response(
                json.dumps({'success': False, 'error': 'Grafana URL is required'}, ensure_ascii=False),
                mimetype='application/json; charset=utf-8',
                status=400
            )
        
        if not api_key:
            current_app.logger.error("No Grafana API key provided in request or environment")
            return Response(
                json.dumps({'success': False, 'error': 'Grafana API key is required'}, ensure_ascii=False),
                mimetype='application/json; charset=utf-8',
                status=400
            )
        
        # Add trailing slash to URL if not present
        if not url.endswith('/'):
            url += '/'
        
        # Make sure we're requesting proper content types
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json, text/plain',
            'Accept-Charset': 'utf-8'
        }
        
        # Test health endpoint
        health_url = f"{url}api/health"
        current_app.logger.info(f"Testing Grafana connection to: {health_url}")
        
        # Use a custom session with encoding control
        session = requests.Session()
        response = session.get(health_url, headers=headers, timeout=10)
        
        # Ensure proper encoding
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            current_app.logger.info(f"Grafana health check successful: {response.status_code}")
            
            # Build a sanitized result with only ASCII-safe characters
            # This avoids encoding issues entirely
            result = {'success': True}
            
            try:
                # Extract only what we need from the health response and sanitize
                health_data = response.json()
                if isinstance(health_data, dict):
                    if 'version' in health_data:
                        result['version'] = str(health_data.get('version', 'Unknown'))
                    if 'database' in health_data:
                        result['database'] = str(health_data.get('database', 'Unknown'))
                
                # Only try to get version and datasources if we need them
                # but keep the response minimal and avoid any complex/nested data
                
                # Simplified success response - avoid any potentially problematic unicode
                return Response(
                    json.dumps({'success': True}, ensure_ascii=True),
                    mimetype='application/json; charset=utf-8',
                    status=200
                )
            except Exception as e:
                current_app.logger.error(f"Error processing Grafana response: {str(e)}")
                return Response(
                    json.dumps({'success': True, 'note': 'Basic connection successful, but additional details unavailable'}, ensure_ascii=True),
                    mimetype='application/json; charset=utf-8',
                    status=200
                )
        else:
            current_app.logger.error(f"Grafana API returned non-200 status: {response.status_code}")
            return Response(
                json.dumps({
                    'success': False, 
                    'error': f'Connection failed with status code: {response.status_code}'
                }, ensure_ascii=True),
                mimetype='application/json; charset=utf-8',
                status=200
            )
            
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error testing Grafana connection: {str(e)}")
        return Response(
            json.dumps({'success': False, 'error': f"Connection error: {str(e)}"}, ensure_ascii=True),
            mimetype='application/json; charset=utf-8',
            status=200
        )
    except Exception as e:
        current_app.logger.error(f"Error testing Grafana connection: {str(e)}")
        return Response(
            json.dumps({'success': False, 'error': f"Unexpected error: {str(e)}"}, ensure_ascii=True),
            mimetype='application/json; charset=utf-8',
            status=200
        )

@settings_bp.route('/api/grafana/test-query', methods=['POST'])
@login_required
def test_grafana_query():
    """
    Test Grafana API query.
    """
    data = request.get_json()
    url = data.get('url')
    api_key = data.get('api_key')
    query = data.get('query')
    
    # If URL or API key is not provided in the request, use environment variables
    if not url or not url.strip():
        url = os.getenv('GRAFANA_URL')
        current_app.logger.info("Using Grafana URL from environment variables")
    
    if not api_key or not api_key.strip():
        api_key = os.getenv('GRAFANA_API_TOKEN')
        current_app.logger.info("Using Grafana API key from environment variables")
    
    # Check for required parameters
    if not url or not url.strip():
        return jsonify({'success': False, 'error': 'Grafana URL is required'})
    
    if not api_key or not api_key.strip():
        return jsonify({'success': False, 'error': 'Grafana API key is required'})
    
    if not query or not query.strip():
        return jsonify({'success': False, 'error': 'Query is required'})
    
    # Ensure URL doesn't end with a slash
    url = url.rstrip('/')
    
    try:
        # Set up headers for API request
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8'
        }
        
        # Execute the query through the Grafana API
        current_time = int(time.time())
        one_hour_ago = current_time - 3600
        
        payload = {
            'queries': [
                {
                    'refId': 'A',
                    'datasource': 'Prometheus',  # Or use a dynamic datasource selection
                    'expr': query,
                    'instant': True
                }
            ],
            'from': str(one_hour_ago * 1000),
            'to': str(current_time * 1000)
        }
        
        response = requests.post(
            f"{url}/api/ds/query",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            # Handle non-success response
            error_text = response.text[:500] if response.text else f"HTTP {response.status_code}"
            return jsonify({
                'success': False,
                'error': f'Query failed: {error_text}'
            })
        
        # Process response to handle any encoding issues
        try:
            result_data = response.json()
            
            # Safely convert to JSON with UTF-8 encoding
            return current_app.response_class(
                json.dumps({
                    'success': True,
                    'results': result_data
                }, ensure_ascii=False),
                mimetype='application/json; charset=utf-8'
            )
        except json.JSONDecodeError as e:
            current_app.logger.error(f"Failed to parse Grafana response: {str(e)}")
            return jsonify({
                'success': False,
                'error': f'Failed to parse response: {str(e)}'
            })
        
    except requests.exceptions.ConnectionError as e:
        current_app.logger.error(f"Grafana connection error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Could not connect to Grafana server. Please check the URL and ensure the server is running.'
        })
    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'error': 'Query timed out. The query may be too complex or the server is busy.'
        })
    except Exception as e:
        # Generic error handler for any issues
        current_app.logger.error(f"Error executing Grafana query: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred with the Grafana query. Please check the logs for details.'
        }) 