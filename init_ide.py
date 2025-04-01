#!/usr/bin/env python3
"""
Initialize IDE settings for the Performance Reporting application.
This script creates the necessary .vscode/settings.json file with the appropriate theme and settings.
"""
import os
import json
from pathlib import Path

def create_settings_json():
    """Create settings.json file for VS Code/Cursor"""
    
    # Create .vscode directory if it doesn't exist
    vscode_dir = Path('.vscode')
    vscode_dir.mkdir(exist_ok=True)
    
    # Define settings content
    settings = {
        # Editor Settings
        "editor.formatOnSave": True,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.tabSize": 2,
        "editor.rulers": [100],
        "editor.wordWrap": "on",
        "editor.renderWhitespace": "boundary",
        "editor.minimap.enabled": True,
        "editor.guides.bracketPairs": True,
        
        # Python Settings
        "python.linting.enabled": True,
        "python.linting.pylintEnabled": True,
        "python.linting.flake8Enabled": True,
        "python.formatting.provider": "black",
        "python.formatting.blackArgs": ["--line-length", "100"],
        "python.testing.pytestEnabled": True,
        "python.testing.unittestEnabled": False,
        "python.testing.nosetestsEnabled": False,
        "python.testing.pytestArgs": [
            "tests"
        ],
        
        # Flask settings
        "[python]": {
            "editor.tabSize": 4,
            "editor.formatOnSave": True,
            "editor.defaultFormatter": "ms-python.python"
        },
        
        # Tailwind CSS Settings
        "css.validate": False,
        "tailwindCSS.emmetCompletions": True,
        "tailwindCSS.includeLanguages": {
            "html": "html",
            "javascript": "javascript",
            "css": "css",
            "jinja-html": "html"
        },
        "tailwindCSS.classAttributes": [
            "class",
            "className",
            "ngClass"
        ],
        "tailwindCSS.colorDecorators": True,
        "editor.quickSuggestions": {
            "strings": True
        },

        # Theme and Color Settings
        "workbench.colorTheme": "Default Dark+",
        "workbench.iconTheme": "material-icon-theme",
        "workbench.colorCustomizations": {
            "sideBar.background": "#1f2937",
            "sideBar.foreground": "#e5e7eb",
            "sideBar.border": "#374151",
            "activityBar.background": "#111827",
            "activityBar.foreground": "#e5e7eb",
            "editor.background": "#ffffff",
            "editor.foreground": "#111827",
            "statusBar.background": "#1f2937",
            "statusBar.foreground": "#e5e7eb"
        },
        
        # Terminal Settings
        "terminal.integrated.defaultProfile.linux": "bash",
        "terminal.integrated.defaultProfile.osx": "zsh",
        "terminal.integrated.defaultProfile.windows": "PowerShell",
        
        # File associations
        "files.associations": {
            "*.html": "jinja-html",
            "*.j2": "jinja-html",
            "*.css": "tailwindcss"
        },
        
        # Exclude directories from search
        "search.exclude": {
            "**/node_modules": True,
            "**/venv": True,
            "**/.git": True,
            "**/__pycache__": True,
            "**/.pytest_cache": True,
            "**/build_reports": True,
            "**/instance": True
        },
        
        # Exclude directories from file explorer
        "files.exclude": {
            "**/__pycache__": True,
            "**/.pytest_cache": True,
            "**/*.pyc": True
        },
        
        # Auto-save settings
        "files.autoSave": "afterDelay",
        "files.autoSaveDelay": 1000,
        
        # Git settings
        "git.enableSmartCommit": True,
        "git.confirmSync": False,
        
        # Additional settings
        "editor.suggestSelection": "first",
        "explorer.confirmDelete": False,
        "explorer.confirmDragAndDrop": False
    }
    
    # Write the settings file
    settings_path = vscode_dir / 'settings.json'
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"Created settings file at: {settings_path.absolute()}")
    return settings_path

def create_recommended_extensions():
    """Create extensions.json file with recommended extensions"""
    vscode_dir = Path('.vscode')
    vscode_dir.mkdir(exist_ok=True)
    
    extensions = {
        "recommendations": [
            "ms-python.python",
            "ms-python.vscode-pylance",
            "esbenp.prettier-vscode",
            "bradlc.vscode-tailwindcss",
            "batisteo.vscode-flask",
            "wholroyd.jinja",
            "pkief.material-icon-theme",
            "streetsidesoftware.code-spell-checker",
            "ms-python.black-formatter",
            "ms-python.flake8"
        ]
    }
    
    extensions_path = vscode_dir / 'extensions.json'
    with open(extensions_path, 'w') as f:
        json.dump(extensions, f, indent=2)
    
    print(f"Created extensions recommendations file at: {extensions_path.absolute()}")
    return extensions_path

def create_launch_config():
    """Create launch.json file for debugging"""
    vscode_dir = Path('.vscode')
    vscode_dir.mkdir(exist_ok=True)
    
    launch_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Flask",
                "type": "python",
                "request": "launch",
                "module": "flask",
                "env": {
                    "FLASK_APP": "app.py",
                    "FLASK_ENV": "development"
                },
                "args": [
                    "run",
                    "--no-debugger",
                    "--no-reload"
                ],
                "jinja": True
            },
            {
                "name": "Python: Current File",
                "type": "python",
                "request": "launch",
                "program": "${file}",
                "console": "integratedTerminal"
            }
        ]
    }
    
    launch_path = vscode_dir / 'launch.json'
    with open(launch_path, 'w') as f:
        json.dump(launch_config, f, indent=2)
    
    print(f"Created launch configuration file at: {launch_path.absolute()}")
    return launch_path

def create_tasks_config():
    """Create tasks.json file for common tasks"""
    vscode_dir = Path('.vscode')
    vscode_dir.mkdir(exist_ok=True)
    
    tasks_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Run Flask App",
                "type": "shell",
                "command": "./start.sh",
                "presentation": {
                    "reveal": "always",
                    "panel": "new"
                },
                "problemMatcher": []
            },
            {
                "label": "Run Tests",
                "type": "shell",
                "command": "make test",
                "presentation": {
                    "reveal": "always",
                    "panel": "new"
                },
                "problemMatcher": []
            },
            {
                "label": "Generate Build Report",
                "type": "shell",
                "command": "make report",
                "presentation": {
                    "reveal": "always",
                    "panel": "new"
                },
                "problemMatcher": []
            }
        ]
    }
    
    tasks_path = vscode_dir / 'tasks.json'
    with open(tasks_path, 'w') as f:
        json.dump(tasks_config, f, indent=2)
    
    print(f"Created tasks configuration file at: {tasks_path.absolute()}")
    return tasks_path

def main():
    """Main function to create all IDE settings"""
    print("Initializing IDE settings for Performance Reporting application...")
    
    settings_path = create_settings_json()
    extensions_path = create_recommended_extensions()
    launch_path = create_launch_config()
    tasks_path = create_tasks_config()
    
    print("\nIDE settings initialized successfully!")
    print("\nRecommended steps:")
    print("1. Install recommended extensions")
    print("2. Reload the IDE")
    print("3. Verify theme is applied correctly")
    print("4. Use integrated terminal to run the application with './start.sh'")

if __name__ == "__main__":
    main() 