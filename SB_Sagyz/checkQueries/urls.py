from django.urls import path
from .views import dashboard_view, query_info_view

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('query/<int:query_id>/', query_info_view, name='query_info'),
]