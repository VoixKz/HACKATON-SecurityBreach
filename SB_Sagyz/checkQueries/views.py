from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ScanHistory, Query
from authApp.models import CustomUser

from botScanner.data_crawler import scrap_data_ip



@login_required
def dashboard_view(request):
    user = get_object_or_404(CustomUser, id=request.user.id)
    scan_history = ScanHistory.objects.filter(user=user).select_related('query')
    context = {
        'user': user,
        'scan_history': scan_history,
    }
    return render(request, 'checkQueries/dashboard.html', context)


@login_required
def query_info_view(request, query_id):
    query = get_object_or_404(Query, id=query_id)
    shodan_result = scrap_data_ip(query.ip_or_domain)
    context = {
        'success': True,
        'ipv4': query.ip_or_domain,
        'status': query.get_status_display(),
        'platforms': shodan_result['platforms'],
        'ports': shodan_result['ports'],
        'os': shodan_result['os'],
        'hostnames': shodan_result['hostnames'],
        'cve_results': query.vulnerabilities.all(),
        'applied_exploits': query.applied_exploits,
        'vulnerable_services_or_apps': query.vulnerable_services_or_apps,
    }
    return render(request, 'checkQueries/query_info.html', context)