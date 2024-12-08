import re, os, openai, requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime



load_dotenv()
openaiApi = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def clean_html(description):
    soup = BeautifulSoup(description, 'html.parser')
    text = soup.get_text(separator='\n').strip()
    cleaned_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    return cleaned_text


def openai_generate_template(raw_data: str) -> str:
    chat_completion = openaiApi.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": raw_data}
        ],
    )
    redata = chat_completion.choices[0].message.content.strip()
    return redata


def format_text_with_openai(text):
    return openai_generate_template(f"Format the following text nicely:\n\n{text}")


def extract_cve_with_openai(description):
    return openai_generate_template(f"Extract the CVE number from the following description: {description}")


def extract_cve_with_regex(description):
    cve_pattern = r'CVE-\d{4}-\d{4,7}'
    matches = re.findall(cve_pattern, description)
    return matches if matches else None


def extract_cve(description):
    cve_regex = extract_cve_with_regex(description)
    if cve_regex:
        return cve_regex[0]
    else:
        return extract_cve_with_openai(description)


def get_cve_details(cve_id):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        published_date = data['vulnerabilities'][0]['cve']['published']
        description = data['vulnerabilities'][0]['cve']['descriptions'][0]['value']
        formatted_date = datetime.strptime(published_date, '%Y-%m-%dT%H:%M:%S.%f').strftime('%B %d, %Y')
        formatted_description = format_text_with_openai(clean_html(description))
        return formatted_date, formatted_description
    else:
        return None, None