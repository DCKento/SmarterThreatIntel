import requests
import openai
from bs4 import BeautifulSoup
import sys

# Ensure openai API key is set
openai.api_key = os.getenv("OPENAI_API_KEY")

def scrape_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text()
    else:
        return "Failed to scrape the website"

def summarize_content(content):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are responsible for summarizing a cybersecurity threat report. Provide a concise summary."
            },
            {
                "role": "user",
                "content": content
            }
        ]
    )
    return response.choices[0].message['content']

def extract_generate_info_fulltext(content):
    info_categories = ["IOCs", "Threat Hunting Techniques", "Detection Rules", "Mitre ATT&CK Framework Alignment", "Mitigations/Controls"]
    extracted_info = {}
    
    # Sample guidance for each category (this will be extended and refined based on actual content and requirements)
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

def cybersecurity_tool_updated(url):
    content = scrape_content(url)
    info = extract_generate_info_fulltext(content)
    return info

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: threatanalysis.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    results = cybersecurity_tool_updated(url)
    for category, info in results.items():
        print(f"{category}:\n{info}\n{'-'*50}\n")
