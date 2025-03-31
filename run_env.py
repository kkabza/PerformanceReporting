#!/usr/bin/env python3
"""
Environment runner for Florida Tax Certificate Sale application.
This script provides a convenient way to run the application in different environments.
"""
import os
import sys
import argparse
import subprocess
import signal
import colorama
from colorama import Fore, Style
from pathlib import Path

# Initialize colorama
colorama.init()

# Constants
ENVIRONMENTS = ['development', 'production', 'testing']
ENV_FILES = {env: f'.env.{env}' for env in ENVIRONMENTS}
ENV_FILES['example'] = '.env.example'

def print_header(text):
    """Print a formatted header."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 60}")
    print(f"{text.center(60)}")
    print(f"{'=' * 60}{Style.RESET_ALL}\n")

def print_error(text):
    """Print an error message."""
    print(f"{Fore.RED}{Style.BRIGHT}ERROR: {text}{Style.RESET_ALL}")

def print_success(text):
    """Print a success message."""
    print(f"{Fore.GREEN}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def print_warning(text):
    """Print a warning message."""
    print(f"{Fore.YELLOW}{Style.BRIGHT}WARNING: {text}{Style.RESET_ALL}")

def print_info(text):
    """Print an info message."""
    print(f"{Fore.BLUE}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def check_env_files():
    """Check if all required environment files exist."""
    missing_files = []
    
    for env, filename in ENV_FILES.items():
        if not Path(filename).exists():
            missing_files.append(filename)
            
    return missing_files

def switch_to_environment(env_name):
    """Switch to the specified environment."""
    env_file = ENV_FILES.get(env_name)
    
    if not env_file or not Path(env_file).exists():
        print_error(f"Environment file {env_file} does not exist")
        return False
    
    # Use the switch_env.py script if it exists
    if Path('switch_env.py').exists():
        result = subprocess.run(['python', 'switch_env.py', env_name])
        return result.returncode == 0
    
    # Otherwise, copy the env file manually
    current_env = Path('.env')
    if current_env.exists():
        current_env.rename('.env.backup')
    
    Path(env_file).copy('.env')
    print_success(f"Switched to {env_name.upper()} environment")
    return True

def run_docker_compose(env_name, detached=False):
    """Run the application using Docker Compose."""
    print_info(f"Starting {env_name} environment with Docker Compose...")
    
    if env_name == 'development':
        service = 'app_dev'
    else:
        service = 'app'
    
    cmd = ['docker-compose', 'up']
    if detached:
        cmd.append('-d')
    cmd.append(service)
    
    try:
        subprocess.run(cmd)
        return True
    except Exception as e:
        print_error(f"Failed to start Docker Compose: {e}")
        return False

def run_flask(env_name, host='0.0.0.0', port=5000):
    """Run the Flask application directly."""
    print_info(f"Starting Flask application in {env_name} environment...")
    
    # Set environment variables
    env = os.environ.copy()
    env['FLASK_APP'] = 'app.py'
    env['FLASK_ENV'] = env_name
    
    if env_name == 'development':
        env['FLASK_DEBUG'] = '1'
    
    # Run Flask
    try:
        flask_cmd = ['flask', 'run', f'--host={host}', f'--port={port}']
        subprocess.run(flask_cmd, env=env)
        return True
    except Exception as e:
        print_error(f"Failed to start Flask: {e}")
        return False

def run_gunicorn(host='0.0.0.0', port=5000, workers=2):
    """Run the application with Gunicorn (production)."""
    print_info("Starting application with Gunicorn (production)...")
    
    try:
        gunicorn_cmd = [
            'gunicorn',
            '--bind', f'{host}:{port}',
            '--workers', str(workers),
            '--timeout', '60',
            'app:app'
        ]
        subprocess.run(gunicorn_cmd)
        return True
    except Exception as e:
        print_error(f"Failed to start Gunicorn: {e}")
        return False

def main():
    """Main entry point of the script."""
    parser = argparse.ArgumentParser(
        description="Run the Florida Tax Certificate Sale application in different environments"
    )
    parser.add_argument(
        'environment',
        choices=ENVIRONMENTS,
        help="The environment to run the application in"
    )
    parser.add_argument(
        '--docker', '-d',
        action='store_true',
        help="Run using Docker Compose"
    )
    parser.add_argument(
        '--detach',
        action='store_true',
        help="Run in detached mode (Docker only)"
    )
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help="Port to bind to (default: 5000)"
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=2,
        help="Number of Gunicorn workers for production (default: 2)"
    )
    
    args = parser.parse_args()
    
    print_header(f"RUNNING APPLICATION IN {args.environment.upper()} ENVIRONMENT")
    
    # Check for missing files
    missing_files = check_env_files()
    if missing_files:
        print_warning("Some environment files are missing:")
        for file in missing_files:
            print(f"  - {file}")
    
    # Switch to the selected environment
    if not switch_to_environment(args.environment):
        return 1
    
    # Run the application
    if args.docker:
        return 0 if run_docker_compose(args.environment, args.detach) else 1
    elif args.environment == 'production':
        return 0 if run_gunicorn(args.host, args.port, args.workers) else 1
    else:
        return 0 if run_flask(args.environment, args.host, args.port) else 1

if __name__ == "__main__":
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print_info("\nShutting down gracefully...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    sys.exit(main()) 