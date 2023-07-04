from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('server.urls')),
    path('api_schema', get_schema_view(title='API Schema', description='Guide for drf'), name='api_schema'),
    path('docs/', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
