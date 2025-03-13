#!/bin/bash

# Simulates Git activity: commits, releases, and environment deployments.
# Uses random sleep intervals up to 2 minutes between activities.

set -e  # Exit on error

# Configure repository (assumes a Git repository is already initialized)
echo "Starting Git Simulation..."

git checkout -b main 2>/dev/null || git checkout main

# Define environments and time tracking
ENVIRONMENTS=("dev" "qa" "prod")
SIMULATION_START=$(date +%s)
SIMULATION_END=$((SIMULATION_START + 3600))  # 1-hour simulation period
LOG_FILE="simulation_timestamps.log"
> "$LOG_FILE"

# Simulate commits, releases, and deployments
for i in {1..20}; do
	# Simulate a commit
	COMMIT_HASH=$(git commit --allow-empty -m "Commit #$i" --date="now" && git rev-parse HEAD)
	COMMIT_TIME=$(git show -s --format=%ci $COMMIT_HASH)
	echo "Commit $COMMIT_HASH at $COMMIT_TIME" | tee -a "$LOG_FILE"
    
	sleep $((RANDOM % 120))  # Random delay up to 2 minutes
    
	# Simulate a release
	RELEASE_TAG="v1.0.$i"
	git tag "$RELEASE_TAG" "$COMMIT_HASH"
	git push origin "$RELEASE_TAG"
	echo "Release $RELEASE_TAG at $COMMIT_TIME" | tee -a "$LOG_FILE"
    
	sleep $((RANDOM % 120))
    
	# Simulate deployments across environments
	for ENV in "${ENVIRONMENTS[@]}"; do
    	DEPLOY_TAG="$ENV-$RELEASE_TAG"
    	git tag "$DEPLOY_TAG" "$COMMIT_HASH"
    	git push origin "$DEPLOY_TAG"
    	DEPLOY_TIME=$(date +"%Y-%m-%d %H:%M:%S")
    	echo "$DEPLOY_TAG deployed at $DEPLOY_TIME" | tee -a "$LOG_FILE"
   	 
    	sleep $((RANDOM % 120))
	done

	# Stop simulation if past end time
	[[ $(date +%s) -ge $SIMULATION_END ]] && break

done

echo "Simulation complete. Log file: $LOG_FILE"
