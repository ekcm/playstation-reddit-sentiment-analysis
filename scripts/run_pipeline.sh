#!/bin/bash

# Exit on any error
set -e

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
BACKEND_DIR="$PROJECT_ROOT/backend"

# Log function for better visibility
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check if Ollama is running
check_ollama() {
    if ! pgrep -x "ollama" > /dev/null; then
        log "Starting Ollama service..."
        open -a Ollama
        # Wait for Ollama to start
        sleep 5
    else
        log "Ollama is already running"
    fi
}

# Function to run a python script with Poetry
run_python_script() {
    local dir=$1
    local script=$2
    log "Running $script in $dir"
    cd "$BACKEND_DIR"
    
    # Export environment variables by reading the file
    while IFS='=' read -r key value; do
        # Skip empty lines and comments
        [[ $key =~ ^[[:space:]]*$ ]] || [[ $key =~ ^# ]] && continue
        # Remove any quotes from the value
        value=$(echo "$value" | tr -d '"'"'")
        export "$key=$value"
    done < "$BACKEND_DIR/.env"
    
    if poetry run python "src/$dir/$script"; then
        log "Successfully completed $script"
    else
        log "Error running $script"
        exit 1
    fi
}

# Main pipeline
log "Starting Reddit data analysis pipeline"

# Step 1: Ensure Poetry environment is set up
log "Setting up Poetry environment"
cd "$BACKEND_DIR"
poetry install --no-root # Skip installing the project itself

# Step 2: Scrape Reddit data
log "Scraping Reddit data"
run_python_script "scraping" "reddit_scraper.py"

# Step 3: Process Reddit data
log "Processing Reddit data"
run_python_script "processing" "data_cleaner.py"

# Step 4: Ensure Ollama is running and run sentiment analysis
log "Checking Ollama service"
check_ollama

log "Running sentiment analysis"
run_python_script "sentiment_analysis" "sentiment_analyzer.py"

log "Reddit data analysis pipeline completed successfully"
