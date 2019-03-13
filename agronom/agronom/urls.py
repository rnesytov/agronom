from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

urlpatterns = [
    path('api/v0_1/', include(f'{settings.PROJECT_NAME}.api_urls')),
    # We may probably run production server in separate thread
    # https://github.com/korfuri/django-prometheus/blob/master/documentation/exports.md#exporting-metrics-in-a-dedicated-thread
    path('', include('django_prometheus.urls')),
    path('accounts/', include('allauth.urls')),
    re_path(r'^\d*\/?$', login_required(TemplateView.as_view(template_name="index.html")), name='index')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += [
        path('admin/', admin.site.urls),
        path('__debug__/', include(debug_toolbar.urls)),
    ]
