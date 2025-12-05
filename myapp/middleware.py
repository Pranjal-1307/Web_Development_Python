from django.contrib.auth import logout
from django.urls import resolve

class LogoutAdminOnPublicPagesMiddleware:
    PUBLIC_URL_NAMES = [
        'landing',
        'home',
        'about',
        'features',
        'contact',
        'country_detail',
        'login',
        'register_employee',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Only act if user is staff (admin/superuser)
        if request.user.is_authenticated and request.user.is_staff:

            try:
                current_url_name = resolve(request.path_info).url_name
            except:
                current_url_name = None

            # Logout admin ONLY on public pages
            if current_url_name in self.PUBLIC_URL_NAMES:
                logout(request)

        return self.get_response(request)
