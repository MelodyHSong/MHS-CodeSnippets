# ☆ Custom Drive Analyzer ☆

A Python-based storage analysis tool designed to identify the largest files and folders on any local drive with high-speed indexing.

## ☆ Features
* **Purpose:** Identifies the top 20 largest files and top 10 largest folders on any local drive.
* **Key Features:** Real-time speed tracking (files/sec), box-styled ASCII tables, and visual disk usage summaries.
* **Drive Selection:** Validates and scans any connected drive (C, D, E, etc.).
* **Detailed File Analysis:** Lists the top 20 largest files with **name, type, and full directory**.
* **Folder Aggregation:** Calculates the size of the top 10 largest folders by summing all sub-contents.
* **Tracking:** Clean, single-line stat tracker showing file count, elapsed time, and **read speed (files/sec)**.
* **Box-Styled UI:** Structured ASCII tables for clear data visualization.
* **Storage Summary:** Visual disk usage bar with Total, Used, and Free space metrics.

## ☆ Prerequisites
Ensure you have Python installed and the `tqdm` library for live stat tracking.

### Installation
```bash
python -m pip install tqdm

```
