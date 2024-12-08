import nmap
import concurrent.futures
import asyncio

nmportscanner = nmap.PortScanner()

async def scan_ports(target: str, portrange: str = '22-8000') -> dict[str, list[tuple[int, str]]]:
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        scan_result = await loop.run_in_executor(executor, sync_scan_ports, target, portrange)
    return scan_result

def sync_scan_ports(target: str, portrange: str) -> dict[str, list[tuple[int, str]]]:
    try:
        nmportscanner.scan(hosts=target, ports=portrange, arguments='-sT')
        scan_result = dict()

        for host in nmportscanner.all_hosts():
            print(nmportscanner[host].hostname())
            print(nmportscanner[host].state())

            for proto in nmportscanner[host].all_protocols():
                current_proto_list = []
                ports = nmportscanner[host][proto].keys()

                for port in sorted(ports):
                    port_state = nmportscanner[host][proto][port]['state']
                    current_proto_list.append((port, port_state))
                scan_result[str(proto)] = current_proto_list

        return scan_result
    except Exception as e:
        print(f"An error occurred: {e}")
        return f'Error: {e}'