import os
from .models import Exploit, Vulnerability
from datetime import datetime
from .sploitus_search import SploitusSearch
from .extract_cve import extract_cve, get_cve_details
from botScanner.bosfor_operator import generate_yaml_from_exploit

def fetch_exploits(query):
    sploit_search = SploitusSearch(query=query, qtype='exploits', sort='date')
    results = sploit_search.exec_query()
    return results

def save_exploits_to_db(exploits):
    for exploit_data in exploits:

        exploit_id = exploit_data.get('exploit_id')
        name = exploit_data.get('name', 'No name')
        date = exploit_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        description = exploit_data.get('description', 'No description')
        repository_url = exploit_data.get('repository_url', 'No repository url')

        if description:
            generate_yaml_from_exploit(description)

        exploit, created = Exploit.objects.get_or_create(
            exploit_id=exploit_id,
            defaults={
                'name': name,
                'publication_date': datetime.strptime(date, '%Y-%m-%d'),
                'description': description,
                'repository_url': repository_url,
                'entrypoint': '',
                'args': '',
            }
        )

        if description:
            cve_id = extract_cve(description)
            if cve_id:

                cve_date, cve_description = get_cve_details(cve_id)
                if cve_date and cve_description:
                    formatted_date = datetime.strptime(cve_date, '%B %d, %Y').strftime('%Y-%m-%d')
                    vulnerability, created = Vulnerability.objects.get_or_create(
                        vulnerability_id=cve_id,
                        defaults={
                            'description': cve_description,
                            'publication_date': formatted_date,
                        }
                    )
                    vulnerability.exploits.add(exploit)
                    vulnerability.save()

                    # static_folder = os.path.join(os.path.dirname(__file__), 'static')
                    # os.makedirs(static_folder, exist_ok=True)
                    # cve_file_path = os.path.join(static_folder, f'cve-{cve_id}.txt')
                    # with open(cve_file_path, 'w') as f:
                    #     f.write(f"{cve_id}\n{formatted_date}\n{cve_description}")
            else:
                print(f"No CVE found in description for exploit ID: {exploit_id}")

def main(query):
    try:
        exploits = fetch_exploits(query)
        save_exploits_to_db(exploits)
    except Exception as e:
        print(f"Error occurred: {e}")