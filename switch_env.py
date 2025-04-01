#!/usr/bin/env python3
"""
Environment switcher for Performance Reporting application.
This script helps switch between development, production, and testing environments.
"""
import os
import sys
import shutil
import argparse
from pathlib import Path
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

def print_header(text):
    """Print a formatted header."""
    print(f"{Fore.CYAN}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def print_error(text):
    """Print an error message."""
    print(f"{Fore.RED}{Style.BRIGHT}ERROR: {text}{Style.RESET_ALL}")

def print_success(text):
    """Print a success message."""
    print(f"{Fore.GREEN}{Style.BRIGHT}SUCCESS: {text}{Style.RESET_ALL}")

def print_warning(text):
    """Print a warning message."""
    print(f"{Fore.YELLOW}{Style.BRIGHT}WARNING: {text}{Style.RESET_ALL}")

def check_env_files():
    """Check if all required environment files exist."""
    env_files = {
        'development': '.env.development',
        'production': '.env.production',
        'testing': '.env.testing',
        'example': '.env.example'
    }
    
    missing_files = []
    
    for env, filename in env_files.items():
        if not Path(filename).exists():
            missing_files.append(filename)
            
    return missing_files

def backup_current_env():
    """Backup the current .env file if it exists."""
    env_path = Path('.env')
    if env_path.exists():
        backup_path = Path('.env.backup')
        shutil.copy2(env_path, backup_path)
        return True
    return False

def switch_to_environment(env_name):
    """Switch to the specified environment by copying the appropriate .env file."""
    valid_envs = ['development', 'production', 'testing']
    
    if env_name not in valid_envs:
        print_error(f"Invalid environment: {env_name}")
        print(f"Valid environments are: {', '.join(valid_envs)}")
        return False
    
    env_file = f'.env.{env_name}'
    
    if not Path(env_file).exists():
        print_error(f"Environment file {env_file} does not exist")
        return False
    
    # Backup current .env
    backed_up = backup_current_env()
    
    # Copy new environment file
    shutil.copy2(env_file, '.env')
    
    print_success(f"Switched to {env_name.upper()} environment")
    if backed_up:
        print_warning("Previous .env file was backed up to .env.backup")
    
    return True

def main():
    """Main entry point of the script."""
    parser = argparse.ArgumentParser(
        description="Switch between development, production, and testing environments"
    )
    parser.add_argument(
        'environment',
        choices=['development', 'production', 'testing'],
        help="The environment to switch to"
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help="Force switch even if environment files are missing"
    )
    
    args = parser.parse_args()
    
    print_header(f"SWITCHING TO {args.environment.upper()} ENVIRONMENT")
    
    # Check for missing files
    missing_files = check_env_files()
    if missing_files and not args.force:
        print_error("Some environment files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        print_warning("Use --force to switch anyway")
        return 1
    
    # Switch to the selected environment
    if switch_to_environment(args.environment):
        print_success(f"Environment switched to {args.environment.upper()}")
        print(f"Run your application with:")
        print(f"  python app.py")
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main()) 