#!/usr/bin/env python3
"""
Checks for uncommitted changes in the repository.
Run this after implementing features to ensure all changes are committed.
"""
import subprocess
import sys
import os
from colorama import init, Fore, Style

# Initialize colorama
init()

def print_header(message):
    """Print a formatted header message."""
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.CYAN}{message.center(60)}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")

def print_error(message):
    """Print a formatted error message."""
    print(f"{Fore.RED}ERROR: {message}{Style.RESET_ALL}")

def print_success(message):
    """Print a formatted success message."""
    print(f"{Fore.GREEN}SUCCESS: {message}{Style.RESET_ALL}")

def print_warning(message):
    """Print a formatted warning message."""
    print(f"{Fore.YELLOW}WARNING: {message}{Style.RESET_ALL}")

def check_for_uncommitted_changes():
    """Check if there are any uncommitted changes in the repo."""
    try:
        # Check if Git is installed
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Check if we're in a git repository
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], 
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Get status of the repository
        result = subprocess.run(["git", "status", "--porcelain"], 
                              check=True, capture_output=True, text=True)
        
        if result.stdout.strip():
            print_header("UNCOMMITTED CHANGES DETECTED")
            print_warning("The following files have uncommitted changes:")
            
            # Parse the status output for a cleaner display
            changes = result.stdout.strip().split('\n')
            for change in changes:
                if change.strip():
                    status = change[:2].strip()
                    filename = change[3:].strip()
                    
                    if status == '??':
                        print(f"{Fore.RED}Untracked:{Style.RESET_ALL} {filename}")
                    elif status == 'M':
                        print(f"{Fore.YELLOW}Modified:{Style.RESET_ALL} {filename}")
                    elif status == 'A':
                        print(f"{Fore.GREEN}Added:{Style.RESET_ALL} {filename}")
                    elif status == 'D':
                        print(f"{Fore.RED}Deleted:{Style.RESET_ALL} {filename}")
                    else:
                        print(f"{status}: {filename}")
            
            print("\nDon't forget to commit these changes before considering the task complete!")
            print_warning("Suggested command: git add . && git commit -m \"[Your descriptive message]\"")
            return False
        else:
            print_success("No uncommitted changes found. All changes are properly tracked!")
            return True
            
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to check git status: {e}")
        return False
    except FileNotFoundError:
        print_error("Git is not installed or not in the PATH.")
        return False

if __name__ == "__main__":
    print_header("CHECKING FOR UNCOMMITTED CHANGES")
    
    if not check_for_uncommitted_changes():
        sys.exit(1)  # Exit with error code if there are uncommitted changes
    
    print("\nAll changes are committed. Good job!")
    sys.exit(0) 