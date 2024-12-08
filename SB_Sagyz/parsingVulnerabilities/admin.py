from django.contrib import admin
from .models import Vulnerability, Exploit

# Register your models here.
admin.site.register(Vulnerability)
admin.site.register(Exploit)