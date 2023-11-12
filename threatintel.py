import requests
from bs4 import BeautifulSoup
import openai
import os
import sys

# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")

def scrape_text(url):
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
    info_categories = ["Summary", "IOCs", "Threat Hunting Techniques", "Detection Rules", "Mitre ATT&CK Framework Alignment", "Mitigations/Controls"]
    extracted_info = {}
    guidance = {
        "Summary": "You are an intelligent assistant expert in transforming cybersecurity threat reports into actionable intelligence. With a focus on providing detailed, accurate, and helpful analysis. Based on the content, you are going to be summarizing a threat report for a Threat Analyst. Write a paragraph that will summarize the main topic and the key findings. Do not generate a bullet points list but rather one or two paragraphs.",
        "IOCs": "You are an intelligent assistant expert in transforming cybersecurity threat reports into actionable intelligence. With a focus on providing detailed, accurate, and helpful analysis. Based on the content, identify or suggest the potential IOCs mentioned in the threat report. Format these so that they are easy to use in further threat hunting activity",
        "Threat Hunting Techniques": "You are an intelligent assistant expert in transforming cybersecurity threat reports into actionable intelligence. With a focus on providing detailed, accurate, and helpful analysis. Based on the content, identify or suggest potential threat hunting techniques related to the report. Keep these threat hunting techniques specific to the report content and with enough detail that an analyst could quickly use the suggestions to start threat hunting in their own environment",
        "Detection Rules": "You are an intelligent assistant expert in transforming cybersecurity threat reports into actionable intelligence. With a focus on providing detailed, accurate, and helpful analysis. Based on the content, identify or suggest potential detection rules. Provide the overall name of the rules and their purpose, then provide an example for how these rules could actually be implemented in an environment. For the detection langauge, use SPL - Seach Processing Language for Splunk",
        "Mitigations/Controls": "You are an intelligent assistant expert in transforming cybersecurity threat reports into actionable intelligence. With a focus on providing detailed, accurate, and helpful analysis. Based on the content, identify or suggest potential mitigation steps or controls. Keep these mitigations specific to the report content and with enough detail that an analyst could quickly use the suggestions to start mitigating against the treats in their own environment. Refrain from providing generic or broad cybersecurity advice where possible",
        "Mitre ATT&CK Framework Alignment": "You are an intelligent assistant expert in transforming cybersecurity threat reports into actionable intelligence. With a focus on providing detailed, accurate, and helpful analysis. Based on the content, identify or suggest the potential Mitre ATT&CK techniques/tactics mentioned or implied. Then match the detection rules created and mitigation techniques identified to each Mitre ATT&CK technique to demonstrate the coverage of these two implementations in improving the security posture with regards to Mitre ATT&CK."
    }
    for category in info_categories:
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
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
    def format_section(content):
        if not content:
            return "Not Found"
        return "<br>".join(content.splitlines())

    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cybersecurity Threat Analysis</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h2 {{ color: #444; }}
            p {{ margin-left: 20px; }}
            .summary {{ margin-bottom: 20px; }}
            .section {{ margin-top: 10px; }}
        </style>
    </head>
    <body>
        <h1>Cybersecurity Threat Analysis</h1>
        <div class="summary">
            <h2>Summary:</h2>
            <p>{summary}</p>
        </div>
        <div class="section">
            <h2>Threat Hunting Techniques:</h2>
            <p>{Threat_Hunting_Techniques}</p>
        </div>
        <div class="section">
            <h2>Detection Rules:</h2>
            <p>{Detection_Rules}</p>
        </div>
        <div class="section">
            <h2>Mitre ATT&CK Framework Alignment:</h2>
            <p>{Mitre_ATTCK_Framework_Alignment}</p>
        </div>
        <div class="section">
            <h2>Mitigations/Controls:</h2>
            <p>{Mitigations_Controls}</p>
        </div>
        <div class="section">
            <h2>IOCs:</h2>
            <p>{IOCs}</p>
        </div>
    </body>
    </html>
    """
    filled_html = html_template.format(
        summary=format_section(results.get("Summary", "")),
        Threat_Hunting_Techniques=format_section(results.get("Threat Hunting Techniques", "")),
        Detection_Rules=format_section(results.get("Detection Rules", "")),
        Mitre_ATTCK_Framework_Alignment=format_section(results.get("Mitre ATT&CK Framework Alignment", "")),
        Mitigations_Controls=format_section(results.get("Mitigations/Controls", "")),
        IOCs=format_section(results.get("IOCs", ""))
    )
    with open("threat_analysis_output.html", "w") as f:
        f.write(filled_html)
    print("HTML report has been generated as 'threat_analysis_output.html'.")

def cybersecurity_tool(url):
    print(f"Scraping URL: {url}")
    full_text = scrape_text(url)
    print("Generating analysis...")
    extracted_info = extract_generate_info_fulltext(full_text)
    generate_html_output(extracted_info)

if __name__ == "__main__":
    try:
        url_to_analyze = sys.argv[1]
        cybersecurity_tool(url_to_analyze)
    except IndexError:
        print("Please provide a URL as an argument.")
    except Exception as e:
        print(f"An error occurred: {e}")
