# Flask Application Template Setup Guide

This document explains how to convert your current project into a reusable template for future Flask applications.

## Method 1: GitHub Template Repository (Recommended)

1. **Clean the current repository**
   ```bash
   # Create a template branch
   git checkout -b template
   
   # Remove project-specific files and data
   rm -rf instance/
   rm -rf build_reports/
   rm -rf __pycache__/
   rm -rf .pytest_cache/
   rm -rf venv/
   
   # Remove .env files except .env.example
   rm -f .env .env.backup
   
   # Commit the cleaned version
   git add .
   git commit -m "Clean repository for template use"
   ```

2. **Create placeholder files for required directories**
   ```bash
   # Create placeholder files
   mkdir -p app/static/{css,js,img}
   mkdir -p app/templates/{pages,layouts,components,errors}
   mkdir -p tests/{unit,integration,functional,api,ui,bdd,sql}
   mkdir -p instance/logs
   mkdir -p build_reports
   
   # Add placeholder files to keep empty directories
   touch app/static/css/.gitkeep
   touch app/static/js/.gitkeep
   touch app/static/img/.gitkeep
   touch instance/logs/.gitkeep
   touch build_reports/.gitkeep
   
   # Add placeholder tests
   touch tests/unit/.gitkeep
   touch tests/integration/.gitkeep
   touch tests/functional/.gitkeep
   touch tests/api/.gitkeep
   touch tests/ui/.gitkeep
   touch tests/bdd/.gitkeep
   touch tests/sql/.gitkeep
   
   # Add .gitignore entries to ignore content but keep directories
   echo "# Ignore contents but keep directory" >> instance/logs/.gitignore
   echo "*" >> instance/logs/.gitignore
   echo "!.gitkeep" >> instance/logs/.gitignore
   echo "!.gitignore" >> instance/logs/.gitignore
   
   echo "# Ignore contents but keep directory" >> build_reports/.gitignore
   echo "*" >> build_reports/.gitignore
   echo "!.gitkeep" >> build_reports/.gitignore
   echo "!.gitignore" >> build_reports/.gitignore
   
   # Commit these placeholders
   git add .
   git commit -m "Add placeholder files for required directories"
   ```

3. **Update .gitignore for template use**
   ```bash
   # Ensure these patterns are in .gitignore
   echo "# Template-specific ignores" >> .gitignore
   echo "instance/*" >> .gitignore
   echo "!instance/logs/" >> .gitignore
   echo "!instance/logs/.gitkeep" >> .gitignore
   echo "!instance/logs/.gitignore" >> .gitignore
   echo "build_reports/*" >> .gitignore
   echo "!build_reports/.gitkeep" >> .gitignore
   echo "!build_reports/.gitignore" >> .gitignore
   echo ".env" >> .gitignore
   echo ".env.*" >> .gitignore
   echo "!.env.example" >> .gitignore
   echo "!.env.development" >> .gitignore
   echo "!.env.testing" >> .gitignore
   echo "!.env.production" >> .gitignore
   echo "!.env.db" >> .gitignore
   
   # Commit gitignore updates
   git add .gitignore
   git commit -m "Update .gitignore for template use"
   ```

4. **Create a project initialization script**
   Create a script that new developers can run to initialize their project based on this template:
   ```bash
   # Create initialization script
   cat > init_project.py << 'EOF'
#!/usr/bin/env python3
"""
Project initialization script for Florida Tax Certificate Sale template.
This script sets up a new project based on this template.
"""
import os
import sys
import shutil
import argparse
import re
import subprocess
from pathlib import Path
import uuid

def print_header(text):
    """Print a formatted header."""
    print(f"\n{'=' * 60}")
    print(f"{text.center(60)}")
    print(f"{'=' * 60}\n")

def print_step(text):
    """Print a step in the initialization process."""
    print(f"→ {text}")

def print_success(text):
    """Print a success message."""
    print(f"✓ {text}")

def print_error(text):
    """Print an error message."""
    print(f"✗ {text}")

def generate_secret_key():
    """Generate a random secret key."""
    return uuid.uuid4().hex

def update_env_files(project_name):
    """Update environment files with project-specific values."""
    env_files = ['.env.example', '.env.development', '.env.testing', '.env.production']
    
    for env_file in env_files:
        if not os.path.exists(env_file):
            print_error(f"Environment file {env_file} not found")
            continue
            
        with open(env_file, 'r') as f:
            content = f.read()
            
        # Replace project name
        content = content.replace("Florida Tax Certificate Sale", project_name)
        
        # Generate new secret keys
        if "SECRET_KEY=" in content:
            content = re.sub(
                r'SECRET_KEY=.*',
                f'SECRET_KEY={generate_secret_key()}',
                content
            )
            
        # Update build version
        if "BUILD_VERSION=" in content:
            import datetime
            today = datetime.datetime.now().strftime("%Y%m%d")
            content = re.sub(
                r'BUILD_VERSION=.*',
                f'BUILD_VERSION=BUILD-{today}-init',
                content
            )
            
        with open(env_file, 'w') as f:
            f.write(content)
            
        print_success(f"Updated {env_file}")

def update_readme(project_name, project_description):
    """Update README.md with project-specific information."""
    if not os.path.exists('README.md'):
        print_error("README.md not found")
        return
        
    with open('README.md', 'r') as f:
        content = f.read()
        
    # Replace project name and description
    content = content.replace("Florida Tax Certificate Sale Auctions", project_name)
    
    # Replace the first paragraph (description)
    content = re.sub(
        r'## Overview\n.*?\n\n',
        f"## Overview\n{project_description}\n\n",
        content,
        flags=re.DOTALL
    )
    
    # Update GitHub links
    github_username = os.path.basename(os.path.dirname(os.getcwd()))
    repo_name = os.path.basename(os.getcwd())
    
    content = re.sub(
        r'github\.com/kkabza/taxsale',
        f'github.com/{github_username}/{repo_name}',
        content
    )
    
    with open('README.md', 'w') as f:
        f.write(content)
        
    print_success("Updated README.md")

def setup_git_repo():
    """Initialize a new Git repository if one doesn't exist."""
    if os.path.exists('.git'):
        response = input("Git repository already exists. Reinitialize? (y/n): ")
        if response.lower() != 'y':
            return

    print_step("Initializing Git repository...")
    subprocess.run(['git', 'init'], check=True)
    
    # Copy pre-commit hooks
    hooks_dir = Path('.git/hooks')
    if hooks_dir.exists():
        for hook in ['pre-commit', 'pre-push']:
            source = Path(f'.git-hooks/{hook}')
            dest = hooks_dir / hook
            
            if source.exists():
                shutil.copy2(source, dest)
                os.chmod(dest, 0o755)  # Make executable
                print_success(f"Installed {hook} hook")

    print_step("Creating initial commit...")
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit from template'], check=True)
    
    print_success("Git repository initialized")

def main():
    """Main entry point of the script."""
    parser = argparse.ArgumentParser(
        description="Initialize a new project based on this template"
    )
    parser.add_argument(
        '--name',
        default=os.path.basename(os.getcwd()),
        help="Project name (default: current directory name)"
    )
    parser.add_argument(
        '--description',
        default="A Flask web application based on the Flask multi-environment template.",
        help="Project description"
    )
    parser.add_argument(
        '--skip-git',
        action='store_true',
        help="Skip Git repository initialization"
    )
    
    args = parser.parse_args()
    
    print_header(f"INITIALIZING PROJECT: {args.name}")
    
    # Create directories
    print_step("Creating required directories...")
    for directory in ['instance/logs', 'build_reports']:
        os.makedirs(directory, exist_ok=True)
        print_success(f"Created {directory}")
    
    # Update environment files
    print_step("Updating environment files...")
    update_env_files(args.name)
    
    # Update README
    print_step("Updating README...")
    update_readme(args.name, args.description)
    
    # Setup Git repo
    if not args.skip_git:
        setup_git_repo()
    
    print_header("PROJECT INITIALIZATION COMPLETE")
    print("Run the following commands to get started:")
    print("  1. python -m venv venv")
    print("  2. source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print("  3. pip install -r requirements-dev.txt")
    print("  4. ./switch_env.py development")
    print("  5. ./run_env.py development")

if __name__ == "__main__":
    main()
EOF

   # Make it executable
   chmod +x init_project.py
   
   # Commit the script
   git add init_project.py
   git commit -m "Add project initialization script"
   ```

5. **Create a directory for Git hooks**
   ```bash
   # Create a directory for Git hooks
   mkdir -p .git-hooks
   
   # Copy the current hooks for template use
   cp .git/hooks/pre-commit .git-hooks/
   cp .git/hooks/pre-push .git-hooks/
   
   # Commit the Git hooks
   git add .git-hooks
   git commit -m "Add Git hooks for template use"
   ```

6. **Push the template branch to GitHub**
   ```bash
   git push -u origin template
   ```

7. **Create a GitHub template repository**
   - Go to your GitHub repository
   - Click on Settings
   - Scroll down to "Template repository" section
   - Check "Template repository" option
   - Now others can create repositories from this template

## Method 2: Cookiecutter Template

For more advanced templating with customization options:

1. Install cookiecutter
   ```bash
   pip install cookiecutter
   ```

2. Create a cookiecutter template structure
   ```bash
   mkdir flask-multienv-template
   cd flask-multienv-template
   ```

3. Create a cookiecutter.json file with template variables
   ```json
   {
     "project_name": "Flask Application",
     "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '-') }}",
     "project_description": "A Flask web application",
     "author_name": "Your Name",
     "author_email": "your.email@example.com",
     "version": "0.1.0",
     "use_sqlalchemy": "y",
     "use_sentry": "y",
     "include_docker": "y"
   }
   ```

4. Convert your project to use cookiecutter variables

## Method 3: Git Project Template

1. Create a separate repository for the template
   ```bash
   # Clone to a new location
   git clone https://github.com/username/taxsale.git flask-template
   cd flask-template
   
   # Remove Git history
   rm -rf .git
   
   # Clean up project-specific files
   rm -rf instance/* build_reports/* __pycache__/ .pytest_cache/ venv/
   
   # Initialize as a new Git repository
   git init
   
   # Add all files
   git add .
   
   # Create initial commit
   git commit -m "Initial template commit"
   
   # Add remote (create a new repository on GitHub first)
   git remote add origin https://github.com/username/flask-template.git
   
   # Push to GitHub
   git push -u origin main
   ```

## Using the Template

### From GitHub Template Repository
1. Click "Use this template" on the GitHub repository page
2. Name your new repository
3. Clone the new repository
4. Run the initialization script
   ```bash
   ./init_project.py --name "My New Project" --description "A detailed description of the project"
   ```

### From Cookiecutter (if implemented)
```bash
cookiecutter gh:username/flask-multienv-template
``` 