from django.contrib import admin
from .models import ScanHistory, Query



admin.site.register(ScanHistory)
admin.site.register(Query)