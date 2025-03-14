#!/usr/bin/env python

import subprocess
import pandas as pd
import argparse
from datetime import datetime, timedelta

# Parse command-line arguments
parser = argparse.ArgumentParser(
    description="Calculate average commit-to-prod lead time."
)
parser.add_argument(
    "--start-time", required=True, help="Simulation start time (YYYY-MM-DD HH:MM:%S)"
)
parser.add_argument(
    "--end-time", required=True, help="Simulation end time (YYYY-MM-DD HH:MM:%S)"
)
args = parser.parse_args()

start_time = datetime.strptime(args.start_time, "%Y-%m-%d %H:%M:%S")
end_time = datetime.strptime(args.end_time, "%Y-%m-%d %H:%M:%S")

# Get all commits within the time window
commit_list = (
    subprocess.run(
        ["git", "log", "--pretty=format:%H %ci"], capture_output=True, text=True
    )
    .stdout.strip()
    .split("\n")
)

lead_time_data = []


def parse_git_timestamp(timestamp):
    """Parses a Git timestamp and removes the timezone offset."""
    return datetime.strptime(" ".join(timestamp.split(" ")[:-1]), "%Y-%m-%d %H:%M:%S")


for line in commit_list:
    parts = line.rsplit(" ", 3)
    commit_hash, commit_time_str = parts[0], " ".join(parts[1:3])
    commit_time = parse_git_timestamp(" ".join(parts[1:]))

    if start_time <= commit_time <= end_time:
        # Find the first prod deployment tag for this commit
        result = subprocess.run(
            ["git", "tag", "--contains", commit_hash], capture_output=True, text=True
        )
        tags = result.stdout.strip().split("\n")
        prod_tags = [tag for tag in tags if tag.startswith("prod-")]

        if prod_tags:
            prod_tag = sorted(prod_tags)[0]  # Earliest prod tag

            # Fetch the actual timestamp of when the tag was created
            deploy_time_str = subprocess.run(
                ["git", "log", "-1", "--format=%ai", "refs/tags/" + prod_tag],
                capture_output=True,
                text=True,
            ).stdout.strip()
            deploy_time = parse_git_timestamp(deploy_time_str)

            lead_time_hours = (deploy_time - commit_time).total_seconds() / 3600
            lead_time_data.append(
                {
                    "Commit": commit_hash,
                    "Commit Time": commit_time,
                    "Prod Deploy Time": deploy_time,
                    "Lead Time (Hours)": lead_time_hours,
                }
            )

# Convert to DataFrame and calculate the average lead time
lead_time_df = pd.DataFrame(lead_time_data)
if not lead_time_df.empty:
    average_lead_time = lead_time_df["Lead Time (Hours)"].mean()
else:
    average_lead_time = None

# Display results
print("Commit-to-Prod Lead Time Analysis")
print(lead_time_df)
print(
    f"Average Commit-to-Prod Lead Time: {average_lead_time:.2f} hours"
    if average_lead_time
    else "No data available in the given time window."
)
