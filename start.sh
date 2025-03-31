#!/bin/bash
# Simple startup script for Florida Tax Certificate Sale Auctions application

# Colors for prettier output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${BLUE}${BOLD}Florida Tax Certificate Sale Auctions${NC}"
echo -e "${BLUE}${BOLD}======================================${NC}"
echo -e "${BOLD}TDD-compliant startup with mandatory build reports${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create virtual environment.${NC}"
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install requirements
echo -e "${BLUE}Installing requirements...${NC}"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install requirements.${NC}"
    exit 1
fi

# Make scripts executable
chmod +x run.py verify_reports.py

# Ensure build_reports directory exists
mkdir -p build_reports

# Set development environment
export FLASK_ENV=development

# === CRITICAL: TDD RULE - BUILD REPORTS ARE MANDATORY ===
echo -e "${BOLD}=== CRITICAL: TDD RULE - BUILD REPORTS ARE MANDATORY ===${NC}"

# Check if we have a recent build report
./verify_reports.py
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}${BOLD}Generating new build report to comply with TDD rules...${NC}"
    make pre-build-test
    
    # Verify again after report generation
    ./verify_reports.py
    if [ $? -ne 0 ]; then
        echo -e "${RED}${BOLD}CRITICAL ERROR: Failed to generate a valid build report!${NC}"
        echo -e "${RED}This violates TDD cursor rules. Cannot continue.${NC}"
        deactivate
        exit 1
    fi
fi

# Start the application
echo -e "${GREEN}${BOLD}Starting application...${NC}"

# Run with post-build verification
./run.py
RESULT=$?

if [ $RESULT -ne 0 ]; then
    echo -e "${RED}Application failed to start or post-build checks failed.${NC}"
    echo -e "${RED}Please check logs for details.${NC}"
    
    # Try running curl to diagnose issues
    echo -e "${YELLOW}Diagnosing connection to web app...${NC}"
    curl -v http://localhost:5000 
    
    # Generate a report even when failed
    echo -e "${YELLOW}Generating post-failure report...${NC}"
    make post-build-test || true
    
    # Deactivate virtual environment when app stops
    deactivate
    exit 1
fi

# Generate post-build test report
echo -e "${BLUE}${BOLD}Generating post-build test report...${NC}"
make post-build-test

echo -e "${GREEN}${BOLD}Application successfully started and all TDD requirements met!${NC}"

# This script will not reach here in normal running, because the app will keep running
# Deactivate virtual environment when app stops
deactivate 