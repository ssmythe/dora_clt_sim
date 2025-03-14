#!/usr/bin/env python

import subprocess
import pandas as pd
import argparse
import re
import matplotlib.pyplot as plt
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


def extract_timestamp_from_tag(tag_name):
    """Extracts deployment timestamp from the tag name (YYYYMMDDHHMMSS)."""
    match = re.search(r"\d{14}$", tag_name)
    if match:
        return datetime.strptime(match.group(0), "%Y%m%d%H%M%S")
    return None


for line in commit_list:
    parts = line.rsplit(
        " ", 4
    )  # Adjusted to properly extract timestamp without timezone
    commit_hash, commit_time_str = parts[0], " ".join(parts[1:3])
    commit_time = datetime.strptime(commit_time_str, "%Y-%m-%d %H:%M:%S")

    if start_time <= commit_time <= end_time:
        # Find the first prod deployment tag for this commit
        result = subprocess.run(
            ["git", "tag", "--contains", commit_hash], capture_output=True, text=True
        )
        tags = result.stdout.strip().split("\n")
        prod_tags = [
            tag for tag in tags if re.match(r"prod-v\d+\.\d+\.\d+-\d{14}$", tag)
        ]

        if prod_tags:
            # Get the prod tag with the earliest timestamp (true first deployment)
            prod_tag = min(prod_tags, key=extract_timestamp_from_tag)

            deploy_time = extract_timestamp_from_tag(prod_tag)

            if deploy_time:
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

# Visualization
if not lead_time_df.empty:
    # Convert lead time dynamically based on the highest lead time value
    max_lead_time = lead_time_df["Lead Time (Hours)"].max() * 60  # Convert to minutes

    if max_lead_time > 1440:
        lead_time_df["Lead Time"] = (
            lead_time_df["Lead Time (Hours)"] / 24
        )  # Convert to days
        time_unit = "Days"
    elif max_lead_time > 60:
        lead_time_df["Lead Time"] = lead_time_df["Lead Time (Hours)"]  # Keep in hours
        time_unit = "Hours"
    else:
        lead_time_df["Lead Time"] = (
            lead_time_df["Lead Time (Hours)"] * 60
        )  # Convert to minutes
        time_unit = "Minutes"

    lead_time_df["Short Commit"] = lead_time_df["Commit"].str[:7]  # Shorten commit hash

    # Calculate the average lead time dynamically
    average_lead_time = lead_time_df["Lead Time"].mean()

    # Create the figure
    plt.figure(figsize=(12, 5))
    plt.plot(
        lead_time_df["Short Commit"],
        lead_time_df["Lead Time"],
        marker="o",
        linestyle="-",
        label="Lead Time",
    )

    # Properly set X-axis as categorical
    plt.xticks(
        ticks=range(len(lead_time_df)),
        labels=lead_time_df["Short Commit"],
        rotation=45,
        ha="right",
    )

    # Draw the average line and label it
    plt.axhline(
        y=average_lead_time,
        color="red",
        linestyle="--",
        label=f"Average: {average_lead_time:.2f} {time_unit}",
    )
    plt.text(
        len(lead_time_df) - 1,
        average_lead_time,
        f"Avg: {average_lead_time:.2f} {time_unit}",
        color="red",
        ha="right",
        va="bottom",
        fontsize=10,
        fontweight="bold",
    )

    # Labels and title
    plt.xlabel("Commit Hash (Shortened)")
    plt.ylabel(f"Lead Time ({time_unit})")
    plt.title("Commit-to-Prod Lead Time Trend")
    plt.legend()
    plt.grid(True)

    # Add more whitespace at the bottom to ensure the x-axis labels are not clipped
    plt.subplots_adjust(bottom=0.25)
    
    # Show the plot
    plt.show()
