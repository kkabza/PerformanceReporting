from flask import Blueprint, render_template, jsonify, request, current_app
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
@login_required
def test_grafana_connection():
    """
    Test Grafana API connection.
    """
    data = request.get_json()
    url = data.get('url')
    api_key = data.get('api_key')
    
    # If URL or API key is not provided in the request, use environment variables
    if not url or not url.strip():
        url = os.getenv('GRAFANA_URL')
        current_app.logger.info("Using Grafana URL from environment variables")
    
    if not api_key or not api_key.strip():
        api_key = os.getenv('GRAFANA_API_TOKEN')
        current_app.logger.info("Using Grafana API key from environment variables")
    
    # Check if we have valid credentials
    if not url or not url.strip():
        return jsonify({'success': False, 'error': 'Grafana URL is required'})
    
    if not api_key or not api_key.strip():
        return jsonify({'success': False, 'error': 'Grafana API key is required'})
    
    # Ensure URL doesn't end with a slash
    url = url.rstrip('/')
    
    try:
        # Test connection to Grafana
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8'
        }
        
        # Test basic health endpoint
        health_response = requests.get(f"{url}/api/health", headers=headers, timeout=10)
        health_response.encoding = 'utf-8'
        
        if health_response.status_code != 200:
            return jsonify({
                'success': False,
                'error': f'Failed to connect to Grafana: HTTP {health_response.status_code}'
            })
        
        try:
            health_data = health_response.json()
            
            # Get additional info about the Grafana instance
            response_data = {
                'success': True,
                'version': str(health_data.get('version', 'Unknown')),
                'database': str(health_data.get('database', 'Unknown'))
            }
            
            # Try to get datasources info
            try:
                datasources_response = requests.get(f"{url}/api/datasources", headers=headers, timeout=10)
                datasources_response.encoding = 'utf-8'
                
                if datasources_response.status_code == 200:
                    datasources = datasources_response.json()
                    response_data['datasources_count'] = len(datasources)
                    
                    # Process datasources safely
                    safe_datasources = []
                    for ds in datasources:
                        # Create a safe copy with only essential fields
                        safe_ds = {
                            'id': ds.get('id', 0),
                            'name': str(ds.get('name', 'Unnamed')),
                            'type': str(ds.get('type', 'Unknown')),
                            'url': str(ds.get('url', ''))
                        }
                        safe_datasources.append(safe_ds)
                    
                    response_data['datasources'] = safe_datasources
                else:
                    current_app.logger.warning(f"Could not fetch datasources: {datasources_response.status_code}")
            except Exception as e:
                current_app.logger.warning(f"Error fetching datasources: {str(e)}")
                # Add error info but continue
                response_data['datasources_error'] = 'Could not fetch datasources'
            
            # Convert to JSON-safe format with ensure_ascii=False to handle Unicode
            return current_app.response_class(
                json.dumps(response_data, ensure_ascii=False),
                mimetype='application/json; charset=utf-8'
            )
        except Exception as e:
            # Handle JSON parsing errors
            current_app.logger.error(f"Error parsing Grafana response: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Error processing Grafana response'
            })
        
    except requests.exceptions.ConnectionError as e:
        error_msg = 'Could not connect to Grafana server. Please check the URL and ensure the server is running.'
        current_app.logger.error(f"Grafana connection error: {str(e)}")
        return jsonify({
            'success': False,
            'error': error_msg
        })
    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'error': 'Connection to Grafana server timed out. The server may be busy or unreachable.'
        })
    except Exception as e:
        # Provide a generic error message for any encoding or other errors
        current_app.logger.error(f"Error testing Grafana connection: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred with the Grafana connection. Please check the logs for details.'
        })

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