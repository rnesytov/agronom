from django.conf import settings

from silk.middleware import SilkyMiddleware
from silk.profiling.profiler import silk_profile


class custom_silk_profile(silk_profile):
    """
    Custom profile class because original class checks for hardcoded name
    'silk.middleware.SilkyMiddleware' in MIDDLEWARE and we use our
    custom 'core.profiling.CustomSilkyMiddleware'
    """

    def _silk_installed(self):
        app_installed = 'silk' in settings.INSTALLED_APPS
        middlewares = getattr(settings, 'MIDDLEWARE', [])
        if not middlewares:
            middlewares = []
        # next line is changed from original
        middleware_installed = 'core.profiling.CustomSilkyMiddleware' in middlewares
        print('!!!', app_installed and middleware_installed)
        return app_installed and middleware_installed


class CustomSilkyMiddleware(SilkyMiddleware):

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        # Only next line differs from default implementation. Profiling added.
        response = response or custom_silk_profile()(self.get_response)(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response
