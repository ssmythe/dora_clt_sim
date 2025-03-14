#!/bin/bash

# Reads simulation log, extracts start and end times, and calls the Python analysis script

LOG_FILE="simulation_timestamps.log"
PYTHON_SCRIPT="calc_clt.py"

# Extract the first commit timestamp
START_TIME=$(grep -m1 -oE "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}" "$LOG_FILE")

# Extract the last deployment timestamp (last line with 'prod-' deployment)
END_TIME=$(grep "prod-" "$LOG_FILE" | tail -n1 | grep -oE "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}")

# Validate extracted times
if [[ -z "$START_TIME" || -z "$END_TIME" ]]; then
    echo "Error: Could not extract start or end times from log file."
    exit 1
fi

# Run the Python script with the extracted time window
python3 "$PYTHON_SCRIPT" --start-time "$START_TIME" --end-time "$END_TIME"
