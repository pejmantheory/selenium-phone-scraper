
# 📞 Selenium Phone Scraper

## Overview

The **Selenium Phone Scraper** is a Python-based project designed to search for businesses near you based on a given keyword (e.g., "pizza near me"). It extracts **business names**, **phone numbers**, and **URLs** from Google search results and saves them into a **CSV file** for further analysis.

This tool provides **real-time updates** in the terminal during execution, making it clear when businesses are being processed and phone numbers are extracted.

---

## Features

- 🌍 **Localized Search**: Searches businesses based on your keyword combined with "near me."
- 📄 **CSV Output**: Saves all extracted data into a structured CSV file:
  - **Business Name**
  - **Phone Number**
  - **Business URL**
- 🔍 **Phone Number Extraction**:
  - Extracts phone numbers from Google search result descriptions.
  - Visits business URLs to scrape additional numbers.
- ⚙️ **Real-Time Feedback**:
  - Displays detailed logs, including:
    - Business names being visited.
    - Phone numbers extracted.
    - Pagination progress.
- 🔐 **CAPTCHA Detection**:
  - Alerts the user if a CAPTCHA is detected during scraping and waits for manual resolution.
- 🌐 **Pagination**:
  - Automatically navigates through multiple pages of Google search results.

---

## Requirements

### **1. Prerequisites**
- **Python 3.8 or higher**
- **Google Chrome** browser installed
- **ChromeDriver** matching your Chrome version ([download here](https://chromedriver.chromium.org/downloads))

### **2. Python Libraries**
Install the required libraries by running:
```bash
pip install selenium
```

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/selenium-phone-scraper.git
   cd selenium-phone-scraper
   ```

2. **Install Dependencies**:
   ```bash
   pip install selenium
   ```

3. **Set Up ChromeDriver**:
   - Download the appropriate version of ChromeDriver for your operating system.
   - Add the ChromeDriver executable to your `PATH`.

---

## Usage

1. Run the script:
   ```bash
   python scraper.py
   ```

2. Enter the search keyword when prompted:
   ```bash
   Enter the keyword to search (e.g., 'pizza'): sushi
   ```

3. The scraper will:
   - Perform a Google search for the keyword (e.g., "sushi near me").
   - Extract business names, phone numbers, and URLs.
   - Save the data into a CSV file named `businesses.csv`.

---

## Output

The script creates a CSV file (`businesses.csv`) in the working directory. The file includes the following columns:

| Business Name       | Phone Number       | URL                        |
|---------------------|--------------------|----------------------------|
| Sushi House         | (123) 456-7890    | https://sushihouse.com     |
| Fresh Sushi Bar     | (987) 654-3210    | https://freshsushibar.com  |

---

## Example Output in the Terminal

```bash
Enter the keyword to search (e.g., 'pizza'): sushi
[INFO] Searching for: sushi near me
[INFO] Search results loaded.

[INFO] Extracting business details...
[INFO] Visiting business: Sushi House - https://sushihouse.com
[INFO] Found phone: (123) 456-7890
[INFO] Visiting business: Fresh Sushi Bar - https://freshsushibar.com
[WARNING] No phone numbers found for Fresh Sushi Bar.
[INFO] Navigating to the next page...

[INFO] Total businesses saved: 2
[INFO] Scraping complete.
```

---

## Features in Development

- **Proxy Rotation**: Automatically switch IP addresses to avoid rate limits.
- **Headless Mode**: Option to run the scraper without opening the browser for faster execution.
- **Advanced CAPTCHA Handling**: Automated CAPTCHA solving mechanisms.

---

## Troubleshooting

### Common Issues

#### 1. **CAPTCHA Detection**
   - If a CAPTCHA is detected, solve it manually in the browser to continue.

#### 2. **Timeout Errors**
   - Ensure a stable internet connection.
   - Verify that ChromeDriver matches your browser version.

#### 3. **No Phone Numbers Found**
   - Some businesses may not display phone numbers on Google search results or their websites.

---

## Contributing

Contributions are welcome! If you'd like to enhance this project, feel free to submit a pull request or open an issue.



