import subprocess, re

def lookup_domain(domain: str) -> tuple[bool, str]:
    if(re.match(r'^(\d{1,3}\.){3}\d{1,3}$', domain)):
        return (True, domain)

    try:
        result = subprocess.run(["nslookup", domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        ip_lines = [line for line in result.stdout.splitlines() if "Address" in line]
        ipv4 = [line.split(":")[-1].strip() for line in ip_lines[1:]]
        return (True, ipv4) if ipv4 else (False, 'not-found')
    except Exception as e:
        return (False, f'Error: {e}')


import socket
def lookup_domain_cross(domain: str) -> tuple[bool, str]:
    if(re.match(r'^(\d{1,3}\.){3}\d{1,3}$', domain)):
        return (True, domain)

    try:
        _, _, ipv4 = socket.gethostbyname_ex(domain)
        return (True, ipv4) if ipv4 else (False, 'not-found')
    except Exception as e:
        return (False, f'Error: {e}')