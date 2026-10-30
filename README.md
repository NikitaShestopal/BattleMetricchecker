# 🛰️ BattleMetrics Telemetry & Activity Tracker

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-Automation-43B02A.svg?logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Anti-Detect](https://img.shields.io/badge/undetected--chromedriver-Bypass-orange.svg)](https://github.com/ultrafunkamsterdam/undetected-chromedriver)

> **Automated real-time telemetry scraper and state monitor engineered to extract dynamic player availability metrics and track server state transitions under anti-bot protection mechanisms.**

---

## 📌 Overview

This project provides an automated, continuous telemetry pipeline that monitors target entities on **BattleMetrics**. It bypasses sophisticated browser fingerprinting and Cloudflare anti-bot checks in a headless environment, periodically polling entity availability and logging formatted state metrics for longitudinal analysis.

### ✨ Key Features

- **🛡️ Anti-Detection Automation:** Leverages `undetected-chromedriver` with tailored browser launch arguments to neutralize modern WAF / bot-fingerprinting systems.
- **🔄 Fault-Tolerant Polling Loop:** Self-healing session lifecycle that automatically spins up, executes targeted DOM queries, and safely destroys headless browser instances to mitigate memory leaks.
- **⚡ Dynamic DOM Traversal:** Robust XPath and fallback locators designed to gracefully handle asynchronous page hydration, network timeouts, and variable server status states.
- **📊 Structured Telemetry Logging:** Continuous data ingestion with persistence to UTF-8 encoded CSV files, complete with standardized UTC timestamps and connection states.

---

## 🏗️ Architecture & Workflow

```       
       [ Target Queue ]
              │
              ▼
 ┌─────────────────────────┐
 │ Undetected ChromeDriver │ ◄── [ Headless Chrome Engine ]
 └────────────┬────────────┘
              │ (Bypass WAF / Load DOM)
              ▼
 ┌─────────────────────────┐
 │   XPath & DOM Parsing   │ ───► Extracts Name & Server Activity
 └────────────┬────────────┘
              │ (Fallback on dynamic states)
              ▼
 ┌─────────────────────────┐
 │  CSV Persistence Layer  │ ───► activity_log.csv (Structured Log)
 └─────────────────────────┘
```


🚀 Tech Stack
Language: Python 3.10+

Browser Automation: Selenium WebDriver, undetected-chromedriver

Data Persistence: Python Standard Library (csv, os, datetime)

Runtime Environment: Headless Google Chrome

⚙️ Installation & Setup
1. Clone the repository
```
git clone [https://github.com/your-username/battlemetrics-activity-tracker.git](https://github.com/your-username/battlemetrics-activity-tracker.git)
cd battlemetrics-activity-tracker
```
2. Set up virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies
```
pip install -r requirements.txt
```

Note: Ensure Google Chrome is installed on your system. If your Chrome executable is in a non-standard directory, verify the binary path in main.py:

```
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
```

🛠️ Configuration & Usage
Update target player endpoints in main.py:

```
URLS = [
    "[https://www.battlemetrics.com/players/46354742](https://www.battlemetrics.com/players/46354742)",
    "[https://www.battlemetrics.com/players/974641218](https://www.battlemetrics.com/players/974641218)",
    # Add more URLs here
]

DELAY_BETWEEN_CYCLES = 60  # Polling interval in seconds
```

Run the tracker:

```
python main.py
```

Output Sample (activity_log.csv)

```
Час;Гравець;Статус;Сервер
2026-10-30 14:15:02;TargetPlayer_01;Online;Rustified.com - EU Main
2026-10-30 14:15:08;TargetPlayer_02;Offline;-
```
