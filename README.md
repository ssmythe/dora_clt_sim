# Commit-to-Prod Lead Time Analysis

## Overview
This project provides a **Git-based simulation** and **analysis tool** for tracking the **lead time from commit to production deployment**. It automates:
- Simulating commits, releases, and deployments across environments (`dev`, `qa`, `prod`)
- Tagging commits with environment-specific deployment timestamps
- Extracting and calculating the **commit-to-prod lead time**
- Visualizing trends with an automatically **generated graph**

## Features
- **Git Simulation**: Generates commits, assigns release tags, and deploys across environments with realistic delays.
- **Immutable Tagging**: Deployment tags include timestamps (`YYYYMMDDHHMMSS`) for precise tracking.
- **Lead Time Calculation**: Determines the time between commit and production deployment.
- **Dynamic Scaling**: Graph automatically adjusts lead time units (**Minutes, Hours, Days**).
- **Trend Visualization**: Generates a time-series graph showing fluctuations in commit-to-prod lead time.

## Installation
### **Prerequisites**
- **Git** installed
- **Python 3.6+** with the following dependencies:  pandas matplotlib
  ```bash
  pip install -r requirements.txt
  ```

## Usage
### **1. Run the Git Simulation**
This script creates **dummy commits**, assigns **release tags**, and simulates **deployments**:
```bash
./dora_git_sim.sh
```
It generates a log (`simulation_timestamps.log`) with commit timestamps and deployment events.

### **2. Parse and Analyze Lead Time**
Run the **analysis script** with a time window:
```bash
./parse_log.sh
```
This extracts commit timestamps and deployment tags, calculates lead time, and generates a **visual graph**.

## Tagging Conventions
| Type         | Format                          | Example                           |
|-------------|--------------------------------|-----------------------------------|
| Commit      | `<commit-hash>`                | `c6b2ba5`                         |
| Release Tag | `v<major>.<minor>.<patch>`    | `v2.0.1`                          |
| Deploy Tag  | `<env>-<release>-YYYYMMDDHHMMSS` | `prod-v2.0.1-20250313173244` |

## Example Workflow
1. **Commit Created** → `c6b2ba5d8e74` (2025-03-13 17:56:25)
2. **Release Tagged** → `v2.0.1`
3. **Deployment to Prod** → `prod-v2.0.1-20250313175710`
4. **Lead Time Calculated** → **3 min 45 sec**

## Visualization
A graph is generated that shows commit-to-prod lead time trends. The graph automatically scales time units and overlays the **average lead time** as a red dashed line.

## Contributing
This project is **open and free** for anyone to use, modify, and improve. Contributions are welcome!

## License
**This project is released with no license.** You are free to use, share, and modify it as needed.