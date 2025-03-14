#!/bin/bash

# Debugging script for Git commit-to-prod analysis

# Output file
DEBUG_LOG="git_debug_output.log"
> "$DEBUG_LOG"  # Clear previous contents

echo "Collecting Git Debug Information..." | tee -a "$DEBUG_LOG"

# Get the current branch
echo -e "\nCurrent Branch:" | tee -a "$DEBUG_LOG"
git branch --show-current | tee -a "$DEBUG_LOG"

# Get the latest commits
echo -e "\nRecent Commits:" | tee -a "$DEBUG_LOG"
git log --pretty=format:"%H %ci" -n 10 | tee -a "$DEBUG_LOG"

# Get all tags and their creation dates
echo -e "\nAll Tags with Creation Dates:" | tee -a "$DEBUG_LOG"
git for-each-ref --format="%(refname:short) %(creatordate:iso)" refs/tags | tee -a "$DEBUG_LOG"

# List all prod tags and their associated commits
echo -e "\nProd Deployment Tags and Associated Commits:" | tee -a "$DEBUG_LOG"
git tag --list "prod-*" | while read tag; do
    echo "Tag: $tag" | tee -a "$DEBUG_LOG"
    git show -s --format="%H %ci" refs/tags/$tag | tee -a "$DEBUG_LOG"
done

# Check what tags contain the latest commits
echo -e "\nChecking Which Tags Contain Recent Commits:" | tee -a "$DEBUG_LOG"
git log --pretty=format:"%H" -n 5 | while read commit; do
    echo "Commit: $commit" | tee -a "$DEBUG_LOG"
    git tag --contains $commit | tee -a "$DEBUG_LOG"
done

# Show detailed information for the latest commit
echo -e "\nDetailed Latest Commit Information:" | tee -a "$DEBUG_LOG"
git show -s --format="Commit: %H%nDate: %ci%nTags: %d" | tee -a "$DEBUG_LOG"

# Output file location
echo -e "\nDebugging information saved to: $DEBUG_LOG" | tee -a "$DEBUG_LOG"