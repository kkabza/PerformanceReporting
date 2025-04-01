from flask import Blueprint, render_template, jsonify, request
from app.routes.auth import login_required
import requests

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

@settings_bp.route('/api/settings/grafana/test-connection', methods=['POST'])
@login_required
def test_grafana_connection():
    data = request.get_json()
    url = data.get('url')
    api_key = data.get('api_key')

    if not url or not api_key:
        return jsonify({'success': False, 'error': 'Missing URL or API key'}), 400

    try:
        # Test connection by trying to get Grafana health status
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(f'{url.rstrip("/")}/api/health', headers=headers, timeout=5)
        
        if response.status_code == 200:
            return jsonify({'success': True})
        else:
            return jsonify({
                'success': False, 
                'error': f'Connection failed with status code: {response.status_code}'
            }), 400

    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Connection error: {str(e)}'
        }), 400

@settings_bp.route('/api/settings/grafana/test-query', methods=['POST'])
@login_required
def test_grafana_query():
    data = request.get_json()
    url = data.get('url')
    api_key = data.get('api_key')
    query = data.get('query')

    if not url or not api_key or not query:
        return jsonify({'success': False, 'error': 'Missing URL, API key, or query'}), 400

    try:
        # Execute query using Grafana API
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.post(
            f'{url.rstrip("/")}/api/ds/query',
            headers=headers,
            json={
                'queries': [{
                    'refId': 'A',
                    'datasource': {'type': 'prometheus'},
                    'expr': query,
                    'instant': True
                }]
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'results': response.json()
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Query failed with status code: {response.status_code}'
            }), 400

    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Query error: {str(e)}'
        }), 400 