from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            return None

        try:
            # settings.AUTO_LOGOUT_DELAY * 60 => converting min to sec
            if datetime.now() - request.session['last_touch'] > timedelta(0, settings.AUTO_LOGOUT_DELAY * 60, 0):
                auth.logout(request)
                del request.session['last_touch']
                return redirect(request, "users:login_user")
        except KeyError:
            pass

        request.session['last_touch'] = datetime.now()
