import requests
from bs4 import BeautifulSoup
import sys
import openai

# Ensure you set the OpenAI API key before using the function
openai.api_key = "YOUR_OPENAI_API_KEY"

def scrape_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        page_content = response.content
        soup = BeautifulSoup(page_content, "html.parser")
        text = soup.get_text()
        return text
    else:
        return "Failed to scrape the website"

def extract_generate_info_fulltext(content):
    info_categories = ["IOCs", "Threat Hunting Techniques", "Detection Rules", "Mitre ATT&CK Framework Alignment", "Mitigations/Controls"]
    extracted_info = {}
    guidance = {
        "IOCs": "Based on the content, identify or suggest the potential IOCs mentioned in the threat report.",
        "Threat Hunting Techniques": "Based on the content, identify or suggest potential threat hunting techniques related to the report.",
        "Detection Rules": "Based on the content, identify or suggest potential detection rules.",
        "Mitre ATT&CK Framework Alignment": "Based on the content, identify or suggest the potential Mitre ATT&CK techniques/tactics mentioned or implied.",
        "Mitigations/Controls": "Based on the content, identify or suggest potential mitigation steps or controls."
    }
    for category in info_categories:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": guidance[category]
                },
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        extracted_info[category] = response.choices[0].message['content']
    return extracted_info

def generate_html_output(results):
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cybersecurity Threat Analysis</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h2 { color: #444; }
            p { margin-left: 20px; }
        </style>
    </head>
    <body>
        <h1>Cybersecurity Threat Analysis</h1>
        <h2>IOCs:</h2>
        <p>{IOCs}</p>
        <h2>Threat Hunting Techniques:</h2>
        <p>{Threat_Hunting_Techniques}</p>
        <h2>Detection Rules:</h2>
        <p>{Detection_Rules}</p>
        <h2>Mitre ATT&CK Framework Alignment:</h2>
        <p>{Mitre_ATTCK_Framework_Alignment}</p>
        <h2>Mitigations/Controls:</h2>
        <p>{Mitigations_Controls}</p>
    </body>
    </html>
    """
    filled_html = html_template.format(
        IOCs=results.get("IOCs", "Not Found"),
        Threat_Hunting_Techniques=results.get("Threat Hunting Techniques", "Not Found"),
        Detection_Rules=results.get("Detection Rules", "Not Found"),
        Mitre_ATTCK_Framework_Alignment=results.get("Mitre ATT&CK Framework Alignment", "Not Found"),
        Mitigations_Controls=results.get("Mitigations/Controls", "Not Found")
    )
    with open("threat_analysis_output.html", "w") as f:
        f.write(filled_html)
    return "HTML report has been generated as 'threat_analysis_output.html'."

def cybersecurity_tool_updated(url):
    content = scrape_content(url)
    results = extract_generate_info_fulltext(content)
    generate_html_output(results)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: threatanalysis.py <URL>")
        sys.exit(1)
    url = sys.argv[1]
    cybersecurity_tool_updated(url)
