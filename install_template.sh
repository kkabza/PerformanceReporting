#!/bin/bash
#
# Flask Multi-Environment Template Installer
# This script installs the template to a new directory and initializes it.
#

set -e  # Exit on error

# ANSI color codes
BOLD="\033[1m"
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"
RESET="\033[0m"

# Print formatted messages
print_header() {
    echo -e "${BOLD}${BLUE}=== $1 ===${RESET}"
}

print_step() {
    echo -e "${CYAN}→ $1${RESET}"
}

print_success() {
    echo -e "${GREEN}✓ $1${RESET}"
}

print_error() {
    echo -e "${RED}✗ $1${RESET}"
}

print_warning() {
    echo -e "${YELLOW}! $1${RESET}"
}

# Check dependencies
check_dependencies() {
    print_step "Checking dependencies..."
    
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install Git and try again."
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3 and try again."
        exit 1
    fi
    
    print_success "All dependencies found."
}

# Parse command line arguments
parse_args() {
    # Default values
    TARGET_DIR=""
    PROJECT_NAME=""
    PROJECT_DESCRIPTION="A Flask web application"
    SKIP_VENV=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --dir)
                TARGET_DIR="$2"
                shift 2
                ;;
            --name)
                PROJECT_NAME="$2"
                shift 2
                ;;
            --description)
                PROJECT_DESCRIPTION="$2"
                shift 2
                ;;
            --skip-venv)
                SKIP_VENV=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Validate required arguments
    if [ -z "$TARGET_DIR" ]; then
        print_error "Target directory is required. Use --dir option."
        show_help
        exit 1
    fi
    
    if [ -z "$PROJECT_NAME" ]; then
        PROJECT_NAME=$(basename "$TARGET_DIR")
        print_warning "Project name not specified. Using '$PROJECT_NAME'."
    fi
}

# Show help message
show_help() {
    echo -e "${BOLD}Flask Multi-Environment Template Installer${RESET}"
    echo
    echo "Usage: $0 --dir TARGET_DIR --name PROJECT_NAME [options]"
    echo
    echo "Options:"
    echo "  --dir DIR             Target directory to install template (required)"
    echo "  --name NAME           Project name (default: directory name)"
    echo "  --description DESC    Project description"
    echo "  --skip-venv           Skip virtual environment creation"
    echo "  --help                Show this help message"
    echo
    echo "Example:"
    echo "  $0 --dir ~/projects/myapp --name \"My App\" --description \"A description of my app\""
}

# Clone template repository
clone_template() {
    print_header "Cloning Template Repository"
    
    if [ -d "$TARGET_DIR" ]; then
        if [ "$(ls -A "$TARGET_DIR" 2>/dev/null)" ]; then
            print_error "Target directory exists and is not empty: $TARGET_DIR"
            exit 1
        fi
    else
        mkdir -p "$TARGET_DIR"
    fi
    
    print_step "Cloning template to $TARGET_DIR..."
    git clone --depth 1 https://github.com/yourusername/flask-multi-environment-template.git "$TARGET_DIR"
    cd "$TARGET_DIR"
    
    # Remove Git history and initialize new repository
    print_step "Removing Git history and initializing new repository..."
    rm -rf .git
    git init
    
    print_success "Template cloned successfully."
}

# Initialize project
initialize_project() {
    print_header "Initializing Project"
    
    print_step "Initializing project with name: $PROJECT_NAME"
    
    VENV_FLAG=""
    if [ "$SKIP_VENV" = true ]; then
        VENV_FLAG="--skip-venv"
    fi
    
    # Run the initialization script
    python3 init_project.py --name "$PROJECT_NAME" --description "$PROJECT_DESCRIPTION" $VENV_FLAG
    
    print_success "Project initialized successfully."
}

# Main function
main() {
    # Show title
    echo
    echo -e "${BOLD}${MAGENTA}Flask Multi-Environment Template Installer${RESET}"
    echo
    
    # Parse command line arguments
    parse_args "$@"
    
    # Check dependencies
    check_dependencies
    
    # Clone template repository
    clone_template
    
    # Initialize project
    initialize_project
    
    # Display success message
    echo
    print_header "Installation Complete"
    echo -e "Your new Flask project has been created in ${BOLD}$TARGET_DIR${RESET}"
    echo
    echo -e "Next steps:"
    echo -e "1. ${BOLD}cd $TARGET_DIR${RESET}"
    echo -e "2. Activate the virtual environment:"
    echo -e "   ${BOLD}source venv/bin/activate${RESET}  # On Windows: venv\\Scripts\\activate"
    echo -e "3. Switch to development environment:"
    echo -e "   ${BOLD}./switch_env.py development${RESET}"
    echo -e "4. Run the application:"
    echo -e "   ${BOLD}./run_env.py development${RESET}"
    echo
    print_success "Happy coding!"
    echo
}

# Run main function
main "$@" 