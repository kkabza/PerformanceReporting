#!/usr/bin/env python3
"""
Project initialization script for the Flask Multi-Environment Template.
This script initializes a new project based on the template by:
1. Updating project-specific files with the provided name and description
2. Setting up Git hooks
3. Creating initial configuration
4. Initializing a virtual environment
5. Installing dependencies
"""

import os
import re
import sys
import argparse
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_step(message):
    """Print a step message in color."""
    print(f"{Colors.BLUE}{Colors.BOLD}==> {message}{Colors.ENDC}")

def print_success(message):
    """Print a success message in color."""
    print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")

def print_warning(message):
    """Print a warning message in color."""
    print(f"{Colors.WARNING}! {message}{Colors.ENDC}")

def print_error(message):
    """Print an error message in color."""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def run_command(command, cwd=None, silent=False):
    """Run a shell command and return its output."""
    try:
        if not silent:
            print(f"{Colors.CYAN}$ {command}{Colors.ENDC}")
        
        process = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
            cwd=cwd
        )
        
        if not silent and process.stdout:
            print(process.stdout)
            
        return process.stdout.strip()
    except subprocess.CalledProcessError as e:
        if not silent:
            print_error(f"Command failed with exit code {e.returncode}")
            if e.stdout:
                print(e.stdout)
            if e.stderr:
                print(e.stderr)
        raise

def update_file_content(file_path, replacements):
    """Update file content with the given replacements."""
    if not os.path.exists(file_path):
        print_warning(f"File not found: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    return True

def setup_git_hooks():
    """Set up Git hooks from the .git-hooks directory."""
    print_step("Setting up Git hooks")
    
    hooks_dir = Path('.git-hooks')
    git_hooks_dir = Path('.git/hooks')
    
    if not hooks_dir.exists():
        print_warning("Git hooks directory not found, skipping")
        return
    
    if not git_hooks_dir.exists():
        git_hooks_dir.mkdir(parents=True, exist_ok=True)
    
    for hook_file in hooks_dir.glob('*'):
        if not hook_file.is_file():
            continue
        
        target_file = git_hooks_dir / hook_file.name
        shutil.copy2(hook_file, target_file)
        os.chmod(target_file, 0o755)  # Make executable
        print_success(f"Installed Git hook: {hook_file.name}")

def create_virtual_environment():
    """Create a virtual environment for the project."""
    print_step("Creating virtual environment")
    
    if os.path.exists('venv'):
        print_warning("Virtual environment already exists, skipping")
        return
    
    try:
        run_command("python -m venv venv")
        print_success("Created virtual environment")
    except subprocess.CalledProcessError:
        print_error("Failed to create virtual environment")
        raise

def install_dependencies():
    """Install project dependencies from requirements files."""
    print_step("Installing dependencies")
    
    # Determine the activate script based on the OS
    if sys.platform == 'win32':
        activate_script = "venv\\Scripts\\activate"
    else:
        activate_script = "source venv/bin/activate"
    
    try:
        run_command(f"{activate_script} && pip install -U pip wheel && "
                   f"pip install -r requirements.txt -r requirements-dev.txt -r requirements-test.txt",
                   shell=True)
        print_success("Installed dependencies")
    except subprocess.CalledProcessError:
        print_error("Failed to install dependencies")
        raise

def initialize_config_files(project_name, project_description):
    """Initialize configuration files with project-specific values."""
    print_step("Initializing configuration files")
    
    # Generate a random secret key
    try:
        import secrets
        secret_key = secrets.token_hex(32)
    except ImportError:
        import random
        import string
        secret_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(64))
    
    # Update .env files
    env_files = ['.env.example', '.env.development', '.env.production', '.env.testing']
    replacements = [
        (r'FLASK_APP_NAME=.*', f'FLASK_APP_NAME="{project_name}"'),
        (r'SECRET_KEY=.*', f'SECRET_KEY="{secret_key}"'),
        (r'APP_DESCRIPTION=.*', f'APP_DESCRIPTION="{project_description}"')
    ]
    
    for env_file in env_files:
        if os.path.exists(env_file):
            if update_file_content(env_file, replacements):
                print_success(f"Updated {env_file}")
    
    # Update config/base.py
    config_base = 'config/base.py'
    if os.path.exists(config_base):
        config_replacements = [
            (r"APP_NAME = '.*'", f"APP_NAME = '{project_name}'"),
            (r"APP_DESCRIPTION = '.*'", f"APP_DESCRIPTION = '{project_description}'")
        ]
        
        if update_file_content(config_base, config_replacements):
            print_success(f"Updated {config_base}")

def update_readme(project_name, project_description):
    """Update README.md with project-specific information."""
    print_step("Updating README.md")
    
    if not os.path.exists('README.md'):
        print_warning("README.md not found, creating new one")
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(f"# {project_name}\n\n{project_description}\n")
        print_success("Created README.md")
        return
    
    replacements = [
        (r'# .*', f'# {project_name}'),
        (r'(?<=\n\n)[^\n#]+(?=\n)', project_description)
    ]
    
    if update_file_content('README.md', replacements):
        print_success("Updated README.md")

def clean_template_files():
    """Remove template-specific files that aren't needed in new projects."""
    print_step("Cleaning template files")
    
    files_to_remove = ['TEMPLATE.md']
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print_success(f"Removed {file}")
    
    # Remove .git-hooks directory after hooks are installed
    if os.path.exists('.git-hooks'):
        shutil.rmtree('.git-hooks')
        print_success("Removed .git-hooks directory")

def main():
    """Main function to initialize the project."""
    parser = argparse.ArgumentParser(description='Initialize a new project from the Flask Multi-Environment Template')
    parser.add_argument('--name', required=True, help='Name of the project')
    parser.add_argument('--description', required=True, help='Brief description of the project')
    parser.add_argument('--skip-venv', action='store_true', help='Skip virtual environment creation')
    parser.add_argument('--skip-deps', action='store_true', help='Skip dependency installation')
    
    args = parser.parse_args()
    
    print(f"{Colors.HEADER}{Colors.BOLD}Initializing project: {args.name}{Colors.ENDC}")
    print(f"{Colors.HEADER}Description: {args.description}{Colors.ENDC}")
    print()
    
    # Ensure we're in the project root
    if not os.path.exists('app') or not os.path.exists('requirements.txt'):
        print_error("This script must be run from the project root directory")
        sys.exit(1)
    
    try:
        # Update project files
        update_readme(args.name, args.description)
        initialize_config_files(args.name, args.description)
        
        # Setup Git
        setup_git_hooks()
        
        # Create virtual environment and install dependencies
        if not args.skip_venv:
            create_virtual_environment()
            
            if not args.skip_deps:
                install_dependencies()
        
        # Clean up template files
        clean_template_files()
        
        # Final success message
        print()
        print_success(f"Project '{args.name}' has been initialized successfully!")
        print()
        print(f"{Colors.BOLD}Next steps:{Colors.ENDC}")
        print("1. Activate the virtual environment:")
        if sys.platform == 'win32':
            print("   > venv\\Scripts\\activate")
        else:
            print("   $ source venv/bin/activate")
        print("2. Switch to development environment:")
        print("   $ ./switch_env.py development")
        print("3. Run the application:")
        print("   $ ./run_env.py development")
        
    except Exception as e:
        print_error(f"Project initialization failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 