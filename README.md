# Smarter Threat Intel

## Purpose

The Cybersecurity Threat Report Analyzer is designed to assist cybersecurity teams in rapidly understanding, extracting, and generating actionable information from threat intelligence reports. These reports, often long-form and detailed, are transformed into easily consumable and actionable formats.

## Description

Threat intelligence reports contain a wealth of information, including details about threat actors, tactics, techniques, and procedures (TTPs), indicators of compromise (IOCs), and more. However, due to their depth and complexity, extracting immediately actionable data can be time-consuming. This tool automates that process, leveraging the power of GPT-4 to summarize, extract, and generate insights from these reports.

### Key Features:
- **Summarization**: Condense lengthy reports into concise summaries.
- **Information Extraction and Generation**: Identify and generate information on:
  - Indicators of Compromise (IOCs)
  - Threat Hunting Techniques
  - Detection Rules
  - Mitre ATT&CK Framework Alignment
  - Mitigation or Controls for Prevention

## Technical Details

### Dependencies:

- Python 3.x
- `requests`: For fetching content from URLs.
- `BeautifulSoup`: For parsing and extracting text from HTML content.
- `openai`: To interact with the OpenAI GPT-4 model.

### Usage:

1. Install the required libraries:
```bash
pip install requests beautifulsoup4 openai
```
2. Ensure you have set up the OpenAI API key. This can be done either by setting it as an environment variable or directly in the script.
3. Run the tool
```bash
python threatanalysis.py "YOUR_THREAT_REPORT_URL"
```

## Limitations:
The tool's accuracy is influenced by the quality, clarity, and structure of the input threat report.
It's essential to validate the extracted/generated content, especially in a critical field like cybersecurity.
