from django.shortcuts import render
from checkQueries.models import Query, ScanHistory
from parsingVulnerabilities.models import Vulnerability

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from botScanner.nslookup import lookup_domain
from botScanner.data_crawler import scrap_data_ip
from botScanner.bosfor_operator import execute_yaml_tester


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def create_query_view(request):
    if request.method == 'POST':
        ipv4raw = str(request.POST.get('ip_or_domain'))
        ipv4final = ipv4raw
        nsrequest = lookup_domain(ipv4raw)
        
        if nsrequest[0]:
            ipv4final = str(nsrequest[1])
        
        shodan_result = scrap_data_ip(ipv4raw)
        
        vulnerabilities = Vulnerability.objects.all()
        cve_results = {}
        vulnerable_services_or_apps = []
        applied_exploits = []
        status = 'secured'
        probed_vulnerabilities = []
        
        mresults = execute_yaml_tester(ipv4final)
        print(f'REERER: {mresults}')
        for vulnerability in vulnerabilities:
            cve_id = vulnerability.vulnerability_id
            for file_name, result in mresults.items():
                if cve_id in file_name:
                    cve_results[cve_id] = result
                    if result and result != 'OK/NO VULNERABILITIES':
                        status = 'vulnerable'
                        probed_vulnerabilities.append(vulnerability)
                        vulnerable_services_or_apps.append(cve_id)
                        for exploit in vulnerability.exploits.all():
                            applied_exploits.append(exploit.name)
        
        if status == 'secured' and any(result != 'OK/NO VULNERABILITIES' for result in cve_results.values()):
            status = 'other'
        
        query = Query.objects.create(
            ip_or_domain=str(ipv4final)[2:-2],
            status=status,
            applied_exploits=', '.join(applied_exploits),
            vulnerable_services_or_apps=', '.join(vulnerable_services_or_apps)
        )
        query.vulnerabilities.set(probed_vulnerabilities)
        query.save()
        
        scan_history = ScanHistory.objects.create(
            user=request.user,
            query=query
        )
        scan_history.save()
        
        context = {
            'success': True,
            'ipv4': str(ipv4final)[2:-2],
            'platforms': shodan_result['platforms'],
            'ports': shodan_result['ports'],
            'os': shodan_result['os'],
            'hostnames': shodan_result['hostnames'],
            'cve_results': cve_results
        }
        
        return render(request, 'botScanner/query_info.html', context)
    return render(request, 'botScanner/create_query.html')


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def vulnerabilities_view(request):
    domain = request.GET.get('domain')
    if domain:
        try:
            query = Query.objects.get(ip_or_domain=domain)
            vulnerabilities = query.vulnerabilities.all()
        except Query.DoesNotExist:
            return Response({'success': False, 'message': 'Domain not found in query database'}, status=404)
    else:
        vulnerabilities = Vulnerability.objects.all()

    data_to_send = {
        'success': True,
        'vulnerabilities': [
            {'name': vulnerability.vulnerability_id, 'description': vulnerability.description}
            for vulnerability in vulnerabilities
        ]
    }
    return Response(data_to_send)