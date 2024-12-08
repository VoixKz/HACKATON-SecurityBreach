import shodan, os

API_KEY = os.getenv('SHODAN_API_KEY')

api = shodan.Shodan(API_KEY)

try:
    api_info = api.info()
    print(f"Plan: {api_info['plan']}")
    print(f"Query Credits: {api_info['query_credits']}")
    print(f"Scan Credits: {api_info['scan_credits']}")
    print(f"Monitored IPs: {api_info['monitored_ips']}")
except shodan.APIError as e:
    print(f"Error: {e}")