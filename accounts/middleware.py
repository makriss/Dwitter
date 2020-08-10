from django.http import HttpResponseRedirect
from django.urls import reverse


class LoginRedirect:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if request.user.is_authenticated and request.path == "/accounts/login":
            return HttpResponseRedirect(reverse('home:homepage'))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
