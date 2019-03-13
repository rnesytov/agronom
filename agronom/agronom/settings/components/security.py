# SECURITY SETTING

SECURE_SSL_REDIRECT = True  # Redirect http request to https

SECURE_SSL_HOST = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # Check that request from external proxy was used

SECURE_HSTS_SECONDS = 24 * 3600  # Browser doesn't connect using http during 1 day, only https.

SECURE_HSTS_INCLUDE_SUBDOMAINS = True   # All subdomaing of our site will be available only by https

SECURE_HSTS_PRELOAD = True  # Allow submitting the site to hardcoded browser HTTPS-only site lists

SECURE_BROWSER_XSS_FILTER = True  # protect from XSS attacks(attacker is sending the
# malicious payload as part of the request

SECURE_CONTENT_TYPE_NOSNIFF = True  # If in our site header correctly defined existing content type(image, gif, etc)
# This function is useful: without it, browser will try to recognize content type by itself, so  malefactor can upload
# script, and say, that's a picture(If our site provide opportunity to upload pictures).

SESSION_COOKIE_SECURE = True  # Cookies will only be served over HTTPS.
# This prevents someone from reading the cookies in a MiTM(Man in the middle) attack
# where they can force the browser to visit a given page.

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
# Just enforce Django default JSONSerializer to be sure unsafe PickleSerializer

SESSION_COOKIE_HTTPONLY = True  # No access to session cookie from JavaScript

CSRF_COOKIE_SECURE = True  # CSRF Cookies will only be served over HTTPS.

REFERRER_POLICY = 'no-referrer'  # Do not set Referer header for requests from pages

X_FRAME_OPTIONS = 'DENY'  # Do not allow show pages in iframe

# email options
# EMAIL_USE_TLS = ...
# EMAIL_USE_SSL = ...
# EMAIL_USE_SSL_CERTIFICATE = ...
# EMAIL_USE_SSL_KEYFILE = ...

# if want to add content-secure-policy, maybe use that? https://github.com/mozilla/django-csp
