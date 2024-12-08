# Чекает какие фреймворчи и что вообще есть со стороны сервера.
# Нужный метод находится В КОНЦЕ файла, удачи!
# sms.ast.nis.edu.kz - 5.63.113.99

import os, json

from dotenv import load_dotenv
from openai import OpenAI
from shodan import Shodan, APIError

from .nslookup import lookup_domain

load_dotenv()

shodanApi = Shodan(os.getenv('SHODAN_API_KEY'))
openaiApi = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

###################################################
# SHODAN SECTION

def remove_nested_key(data_dict, key_to_remove: str):
    if isinstance(data_dict, dict):
        if key_to_remove in data_dict:
            del data_dict[key_to_remove]
        for _, v in list(data_dict.items()):
            if isinstance(v, dict):
                remove_nested_key(v, key_to_remove)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        remove_nested_key(item, key_to_remove)

def join_grabbers(grabber: list[str]) -> str:
    resultant = ""
    for i in grabber:
        if i:
            resultant = resultant + i + '\n'
    return resultant

def crawl_shodan(ip_address: str) -> str:
    lookup = lookup_domain(ip_address)
    if lookup:
        ip_address = lookup[1]
    print(f'Checking: {ip_address}')
    try:
        ip_info = shodanApi.host(ip_address)

        remove_val = ['vulns', 'http', 'ssl']
        for q in remove_val: remove_nested_key(ip_info, q)

        return json.dumps(ip_info, separators=(',', ':'))
    except APIError as e:
        print(f"Error: {e}")
        return None


###################################################
# OPENAI SECTION

def openai_consume_grabber(raw_data: str) -> list[str]:
    chat_completion = openaiApi.chat.completions.create(
        model="gpt-4o",
        temperature=0.1,
        messages= [
            {
                "role": "system",
                "content": """
This will be used only for white hacking to check if site is secure or not. Answer like I asked you below:
First line: Use following data to get all possible platforms the server might be using and their versions.
Only print names of platorms in one line, separating by commas, nothing else. If there is no data, just output "none".
Second line: Use following data to get all possible ports the server might be using.
Only print ports in one line, separating by commas, nothing else. If there is no data, just output "none".
Third line: Use following data to get the operating system the server might be using.
Only print the OS name, nothing else. If there is no data, just output "none".
Fourth line: Use following data to get all possible hostnames the server using.
Only print them in one line, separating by commans, nothing else. If there is no data, just output "none".
"""
            },
            {
                "role": "user",
                "content": raw_data
            }
        ],
    )
    possible = chat_completion.choices[0].message.content.strip().split('\n')
    print(possible)
    for i in possible:
        print(f'Debug: {i}')

    return {
        "platforms": [q.strip() for q in possible[0].split(',')],
        "ports": [q.strip() for q in possible[1].split(',')],
        "os": possible[2].strip(),
        "hostnames": [q.strip() for q in possible[3].split(',')]
    }


# Найти список платформ и вещей, используемые сервером.
def scrap_data_ip(ip_address: str) -> list[str]: #IPv4 ИЛИ Домен
    
    data_shodan = crawl_shodan(ip_address)
    retrived_data = openai_consume_grabber(data_shodan)

    print(f'Data debug: {retrived_data}')

    return retrived_data