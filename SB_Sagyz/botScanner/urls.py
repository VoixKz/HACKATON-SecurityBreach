from django.urls import path
from .views import vulnerabilities_view, create_query_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create_query_view/', create_query_view, name='create_query'),
    path('vulnerabilities/', vulnerabilities_view, name='vulnerabilities'),
]