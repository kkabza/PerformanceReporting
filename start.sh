#!/bin/bash
# Simple startup script for Florida Tax Certificate Sale Auctions application

# Colors for prettier output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Florida Tax Certificate Sale Auctions${NC}"
echo -e "${BLUE}======================================${NC}"

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

# Make run.py executable
chmod +x run.py

# Ensure build_reports directory exists
mkdir -p build_reports

# Set development environment
export FLASK_ENV=development

# Check if we have a recent test report
REPORT_COUNT=$(ls -1 build_reports/test-summary-*.txt 2>/dev/null | wc -l)
if [ "$REPORT_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}No build reports found. Running pre-build tests...${NC}"
    python -c "from app.utils.test_reporter import create_build_report; create_build_report('pre-build')"
    if [ $? -ne 0 ]; then
        echo -e "${RED}Warning: Failed to create build report.${NC}"
        echo -e "${YELLOW}Continuing with application startup...${NC}"
    else
        echo -e "${GREEN}Pre-build tests completed and report generated.${NC}"
    fi
else
    LATEST_REPORT=$(ls -t build_reports/test-summary-*.txt | head -1)
    REPORT_TIME=$(stat -c %Y "$LATEST_REPORT" 2>/dev/null || stat -f %m "$LATEST_REPORT")
    CURRENT_TIME=$(date +%s)
    
    # Check if latest report is more than 24 hours old
    if [ $(($CURRENT_TIME - $REPORT_TIME)) -gt 86400 ]; then
        echo -e "${YELLOW}Build report is more than 24 hours old. Running pre-build tests...${NC}"
        python -c "from app.utils.test_reporter import create_build_report; create_build_report('pre-build')"
        if [ $? -ne 0 ]; then
            echo -e "${RED}Warning: Failed to create build report.${NC}"
            echo -e "${YELLOW}Continuing with application startup...${NC}"
        else
            echo -e "${GREEN}Pre-build tests completed and report generated.${NC}"
        fi
    else
        echo -e "${GREEN}Recent build report exists: $LATEST_REPORT${NC}"
    fi
fi

# Start the application
echo -e "${GREEN}Starting application...${NC}"

# Run with post-build verification
./run.py
RESULT=$?

if [ $RESULT -ne 0 ]; then
    echo -e "${RED}Application failed to start or post-build checks failed.${NC}"
    echo -e "${RED}Please check logs for details.${NC}"
    
    # Try running curl to diagnose issues
    echo -e "${YELLOW}Diagnosing connection to web app...${NC}"
    curl -v http://localhost:5000 
    
    # Deactivate virtual environment when app stops
    deactivate
    exit 1
fi

# Generate post-build test report
echo -e "${BLUE}Generating post-build test report...${NC}"
python -c "from app.utils.test_reporter import create_build_report; create_build_report('post-build')"

# Deactivate virtual environment when app stops
deactivate 