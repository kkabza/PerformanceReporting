from flask import Blueprint, render_template, jsonify, request, Response, current_app
from app.routes.auth import login_required
import requests
import os
import time
import json
import datetime
import csv
import io
import re

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
    
    # More detailed logging of the request
    current_app.logger.info(f"Raw received query: '{query}'")
    current_app.logger.info(f"Query type: {type(query)}")
    current_app.logger.info(f"Query length: {len(query) if query else 0}")
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
    
    # Clean up the query - specifically for InfluxDB queries
    query = query.strip()
    current_app.logger.info(f"Cleaned query: '{query}'")
    
    # Special handling for InfluxDB SHOW MEASUREMENTS - this often fails with the default Grafana API
    is_influxdb_show_command = query.upper().startswith('SHOW ') and 'FROM' not in query.upper()
    current_app.logger.info(f"Detected as InfluxDB SHOW command: {is_influxdb_show_command}")
    
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
        
        # Adjust payload for InfluxDB if needed
        payload = {
            'queries': [
                {
                    'refId': 'A',
                    'datasourceId': 1,  # Default datasource
                    'expr': query,
                    'instant': True
                }
            ],
            'from': str(one_hour_ago * 1000),
            'to': str(current_time * 1000)
        }
        
        # For InfluxDB queries, add extra parameters
        if is_influxdb_show_command:
            payload['queries'][0]['rawQuery'] = True
            payload['queries'][0]['query'] = query
            
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
        current_app.logger.info(f"Raw response content: {response.text[:200]}...")
        
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
                
                # Check for InfluxDB specific errors in the response
                if 'results' in result_data and 'results' in result_data['results']:
                    if 'error' in result_data['results']['A']:
                        error_msg = result_data['results']['A']['error']
                        current_app.logger.error(f"InfluxDB error in response: {error_msg}")
                        
                        # If it's a parsing error with SHOW MEASUREMENTS, provide specific guidance
                        if 'SHOW MEASUREMENTS' in query.upper() and 'found FROM' in error_msg:
                            return jsonify({
                                'success': False,
                                'error': 'InfluxDB query syntax error: The server expected a pure "SHOW MEASUREMENTS" command without additional clauses.',
                                'details': error_msg,
                                'query_sent': query,
                                'suggestion': 'Try entering only "SHOW MEASUREMENTS" without any additional text.'
                            })
                        
                        return jsonify({
                            'success': False,
                            'error': f'InfluxDB query error: {error_msg}',
                            'query_sent': query
                        })
                
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
                'error': f'Query failed: {error_text}',
                'query_sent': query
            })
            
        except ValueError as e:
            # Handle non-JSON responses
            current_app.logger.error(f"Failed to parse Grafana response: {str(e)}")
            current_app.logger.error(f"Response content: {response.text[:500]}")
            
            # Return specific error for invalid JSON
            return jsonify({
                'success': False,
                'error': f'Unexpected token \'{str(e)}\', "{response.text[:20]}..." is not valid JSON',
                'html_response': response.text[:500],
                'query_sent': query
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
            'error': f'An error occurred with the Grafana query: {str(e)}',
            'query_sent': query
        }) 

@settings_bp.route('/grafana/dashboard-info', methods=['POST'])
def get_grafana_dashboard():
    """Retrieves information about a Grafana dashboard using the Grafana API."""
    data = request.json
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    url = data.get('url', '')
    api_key = data.get('api_key', '')
    dashboard_uid = data.get('dashboard_uid', '')
    
    # Validate required parameters
    if not url:
        return jsonify({'success': False, 'error': 'Grafana URL is required'}), 400
    if not api_key:
        return jsonify({'success': False, 'error': 'Grafana API key is required'}), 400
    if not dashboard_uid:
        return jsonify({'success': False, 'error': 'Dashboard UID is required'}), 400
    
    # Ensure URL doesn't end with a slash
    if url.endswith('/'):
        url = url[:-1]
    
    # Create the full API URL
    api_url = f"{url}/api/dashboards/uid/{dashboard_uid}"
    
    current_app.logger.info(f"Fetching dashboard info from: {api_url}")
    
    try:
        # Make the API request to Grafana
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(api_url, headers=headers, timeout=10)
        
        # Log the response status and headers
        current_app.logger.info(f"Grafana API Response Status: {response.status_code}")
        current_app.logger.info(f"Response Headers: {dict(response.headers)}")
        
        # Check for successful response
        if response.status_code == 200:
            try:
                result = response.json()
                return jsonify({'success': True, 'data': result})
            except ValueError as e:
                # Handle JSON parsing error
                current_app.logger.error(f"Failed to parse JSON response: {str(e)}")
                return jsonify({
                    'success': False, 
                    'error': 'Failed to parse JSON response',
                    'details': str(e)
                }), 500
        else:
            # Handle error response
            try:
                error_data = response.json()
                error_message = error_data.get('message', 'Unknown error')
            except:
                error_message = f"HTTP error {response.status_code}"
                
            return jsonify({
                'success': False,
                'error': f"Grafana API error: {error_message}",
                'status': response.status_code
            }), response.status_code
    
    except requests.exceptions.ConnectionError:
        return jsonify({'success': False, 'error': 'Failed to connect to Grafana API'}), 500
    except requests.exceptions.Timeout:
        return jsonify({'success': False, 'error': 'Request to Grafana API timed out'}), 500
    except Exception as e:
        current_app.logger.error(f"Error fetching dashboard info: {str(e)}")
        return jsonify({'success': False, 'error': f'Error: {str(e)}'}), 500 

@settings_bp.route('/grafana/snapshot-info', methods=['POST'])
def get_grafana_snapshot():
    """Retrieves snapshot data from Grafana using the Grafana API."""
    try:
        current_app.logger.info(f"Grafana snapshot info requested")
        
        # Get data from request
        try:
            data = request.get_json()
            if data:
                # Log details but mask API key
                safe_data = {k: (v if k != 'api_key' else f"{'*' * min(10, len(v))}") for k, v in data.items()}
                current_app.logger.info(f"Request JSON data: {safe_data}")
            else:
                current_app.logger.error("No JSON data in request body")
        except Exception as e:
            current_app.logger.error(f"Failed to parse JSON: {str(e)}")
            return jsonify({
                'success': False, 
                'error': 'Invalid JSON in request',
                'details': str(e)
            }), 400
        
        if not data:
            current_app.logger.error("No data provided in request")
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        url = data.get('url', '')
        api_key = data.get('api_key', '')
        snapshot_key = data.get('snapshot_key', '')
        
        # Log details about what we received
        current_app.logger.info(f"URL: {url}")
        current_app.logger.info(f"API key length: {len(api_key) if api_key else 0}")
        current_app.logger.info(f"Snapshot key: {snapshot_key}")
        
        # Validate required parameters
        if not url:
            current_app.logger.error("No Grafana URL provided")
            return jsonify({'success': False, 'error': 'Grafana URL is required'}), 400
        if not api_key:
            current_app.logger.error("No Grafana API key provided")
            return jsonify({'success': False, 'error': 'Grafana API key is required'}), 400
        if not snapshot_key:
            current_app.logger.error("No snapshot key provided")
            return jsonify({'success': False, 'error': 'Snapshot key is required'}), 400
        
        # Parse URL properly
        if url.startswith('http://'):
            url = url[7:]
            protocol = 'http'
        elif url.startswith('https://'):
            url = url[8:]
            protocol = 'https'
        else:
            protocol = 'http'  # Default to HTTP
            
        # Ensure URL doesn't end with a slash
        url = url.rstrip('/')
        full_url = f"{protocol}://{url}"
        
        # Create the full API URL for snapshots
        api_url = f"{full_url}/api/snapshots/{snapshot_key}"
        
        current_app.logger.info(f"Fetching snapshot info from: {api_url}")
        
        try:
            # Make the API request to Grafana
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Accept': 'application/json'
            }
            
            current_app.logger.info(f"Request headers: {{'Authorization': 'Bearer ****', 'Accept': 'application/json'}}")
            
            # Disable SSL verification for testing
            verify_ssl = False  # Set to False for development with self-signed certs
            current_app.logger.info(f"SSL verification: {verify_ssl}")
            
            response = requests.get(
                api_url, 
                headers=headers, 
                timeout=10,
                verify=verify_ssl
            )
            
            # Log the response status
            current_app.logger.info(f"Grafana API Response Status: {response.status_code}")
            current_app.logger.info(f"Response Headers: {dict(response.headers)}")
            
            # Sample of response content for debugging (first 200 chars)
            content_preview = response.text[:200] + "..." if len(response.text) > 200 else response.text
            current_app.logger.info(f"Response content preview: {content_preview}")
            
            # Check for successful response
            if response.status_code == 200:
                try:
                    result = response.json()
                    # Log that we got a valid response
                    current_app.logger.info(f"Successfully parsed snapshot data")
                    return jsonify({'success': True, 'data': result})
                except ValueError as e:
                    # Handle JSON parsing error
                    current_app.logger.error(f"Failed to parse JSON response: {str(e)}")
                    current_app.logger.error(f"Response content: {response.text[:500]}")
                    return jsonify({
                        'success': False, 
                        'error': 'Failed to parse JSON response',
                        'details': str(e),
                        'content_preview': response.text[:500]
                    }), 500
            else:
                # Handle error response
                try:
                    error_data = response.json()
                    error_message = error_data.get('message', 'Unknown error')
                    current_app.logger.error(f"Error from Grafana API: {error_message}")
                except:
                    error_message = f"HTTP error {response.status_code}"
                    current_app.logger.error(f"Non-JSON error response: {response.text[:200]}")
                    
                # Handle 401/403 errors specially
                if response.status_code in (401, 403):
                    return jsonify({
                        'success': False,
                        'error': f"Authentication failed: {error_message}",
                        'status': response.status_code,
                        'content_preview': response.text[:200]
                    }), response.status_code
                else:
                    return jsonify({
                        'success': False,
                        'error': f"Grafana API error: {error_message}",
                        'status': response.status_code,
                        'content_preview': response.text[:200]
                    }), response.status_code
        
        except requests.exceptions.ConnectionError as e:
            current_app.logger.error(f"Connection error: {str(e)}")
            return jsonify({'success': False, 'error': f'Failed to connect to Grafana API: {str(e)}'}), 500
        except requests.exceptions.Timeout as e:
            current_app.logger.error(f"Request timeout: {str(e)}")
            return jsonify({'success': False, 'error': f'Request to Grafana API timed out: {str(e)}'}), 500
        except Exception as e:
            current_app.logger.error(f"Error fetching snapshot info: {str(e)}")
            return jsonify({'success': False, 'error': f'Error: {str(e)}'}), 500
    except Exception as e:
        current_app.logger.error(f"Unhandled exception in get_grafana_snapshot: {str(e)}")
        return jsonify({'success': False, 'error': f'Unhandled server error: {str(e)}'}), 500 

@settings_bp.route('/grafana/export-csv', methods=['POST'])
def export_panel_csv():
    """
    Export panel data as CSV using Grafana API
    """
    try:
        payload = request.json
        
        # Validate required parameters
        required_fields = ['url', 'api_key', 'dashboard_uid', 'panel_id', 'from', 'to']
        for field in required_fields:
            if field not in payload or not payload[field]:
                return jsonify({'status': 'error', 'message': f'Missing required field: {field}'}), 400
        
        # Extract parameters
        grafana_url = payload['url'].rstrip('/')
        api_key = payload['api_key']
        dashboard_uid = payload['dashboard_uid']
        panel_id = payload['panel_id']
        from_time = payload['from']
        to_time = payload['to']
        
        # Log the export action
        current_app.logger.info(f"Exporting CSV for dashboard {dashboard_uid}, panel {panel_id}")
        
        # Step 1: Get the dashboard data to extract the panel query
        dashboard_url = f"{grafana_url}/api/dashboards/uid/{dashboard_uid}"
        dashboard_headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        dashboard_response = requests.get(dashboard_url, headers=dashboard_headers)
        if dashboard_response.status_code != 200:
            current_app.logger.error(f"Error fetching dashboard: {dashboard_response.text}")
            return jsonify({'status': 'error', 'message': f'Failed to fetch dashboard: {dashboard_response.status_code}'}), 500
        
        dashboard_data = dashboard_response.json()
        
        # Find the panel based on panel_id
        panel = None
        for p in dashboard_data.get('dashboard', {}).get('panels', []):
            if str(p.get('id')) == str(panel_id):
                panel = p
                break
        
        if not panel:
            for p in dashboard_data.get('dashboard', {}).get('panels', []):
                for child in p.get('panels', []):
                    if str(child.get('id')) == str(panel_id):
                        panel = child
                        break
                if panel:
                    break
        
        if not panel:
            return jsonify({'status': 'error', 'message': f'Panel with ID {panel_id} not found in dashboard'}), 404
        
        # Get datasource info
        datasource = panel.get('datasource')
        datasource_uid = None
        
        if isinstance(datasource, dict):
            datasource_uid = datasource.get('uid')
        else:
            # For older Grafana versions or when datasource is referenced by name
            datasource_url = f"{grafana_url}/api/datasources/name/{datasource}"
            datasource_response = requests.get(datasource_url, headers=dashboard_headers)
            
            if datasource_response.status_code == 200:
                datasource_uid = datasource_response.json().get('uid')
            else:
                current_app.logger.warning(f"Could not get datasource by name, using default")
        
        # Step 2: Construct query to get data from datasource
        query_data = {
            "queries": [
                {
                    "refId": target.get("refId", "A"),
                    "datasource": {
                        "type": "influxdb",
                        "uid": datasource_uid
                    },
                    "query": target.get("query", ""),
                    "rawQuery": True
                } for target in panel.get("targets", []) if target.get("query")
            ],
            "range": {
                "from": from_time,
                "to": to_time,
                "raw": {
                    "from": from_time,
                    "to": to_time
                }
            },
            "from": from_time,
            "to": to_time
        }
        
        # Step 3: Execute the query
        query_url = f"{grafana_url}/api/ds/query"
        query_response = requests.post(
            query_url,
            headers=dashboard_headers,
            json=query_data
        )
        
        if query_response.status_code != 200:
            current_app.logger.error(f"Error querying datasource: {query_response.text}")
            return jsonify({'status': 'error', 'message': f'Failed to query datasource: {query_response.status_code}'}), 500
        
        query_result = query_response.json()
        
        # Step 4: Process the data into CSV format
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Extract data from the response
        has_written_header = False
        rows_written = 0
        
        for result in query_result.get('results', {}).values():
            for frame in result.get('frames', []):
                columns = []
                data = []
                
                # Extract column names from schema
                for field in frame.get('schema', {}).get('fields', []):
                    columns.append(field.get('name', f"Column{len(columns)}"))
                
                # Extract data values
                for idx, field in enumerate(frame.get('data', {}).get('values', [])):
                    if idx == 0 and columns[idx].lower() == 'time':
                        # Convert timestamps to readable format
                        data.append([
                            datetime.datetime.fromtimestamp(val / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                            if isinstance(val, (int, float)) else val
                            for val in field
                        ])
                    else:
                        data.append(field)
                
                # Write header row if not already written
                if columns and not has_written_header:
                    writer.writerow(columns)
                    has_written_header = True
                
                # Transpose data for CSV rows
                if data:
                    for i in range(len(data[0])):
                        row = [col[i] if i < len(col) else '' for col in data]
                        writer.writerow(row)
                        rows_written += 1
        
        if rows_written == 0:
            current_app.logger.warning("No data returned from query")
            # If no data, write header row at minimum
            if not has_written_header and panel.get('targets'):
                sample_query = panel.get('targets')[0].get('query', '')
                # Try to extract field names from the query
                field_match = re.search(r'SELECT\s+(.*?)\s+FROM', sample_query, re.IGNORECASE)
                if field_match:
                    fields = [f.strip() for f in field_match.group(1).split(',')]
                    writer.writerow(['time'] + fields)
                else:
                    writer.writerow(['time', 'value'])
        
        # Return CSV as downloadable response
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=panel_{panel_id}_export.csv'}
        )
        
    except Exception as e:
        current_app.logger.error(f"Error exporting CSV: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Error exporting CSV: {str(e)}'}), 500 