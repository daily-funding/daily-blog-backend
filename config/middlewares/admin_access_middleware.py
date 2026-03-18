from django.shortcuts import redirect
from django.urls import reverse


class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.admin_login_path = reverse("admin:login")

    def __call__(self, request):
        path = request.path

        if not path.startswith("/admin/"):
            return self.get_response(request)

        if not request.user.is_authenticated:
            if path != self.admin_login_path:
                return redirect(
                    f"{self.admin_login_path}?next={request.get_full_path()}"
                )
            return self.get_response(request)

        if not request.user.is_staff:
            return redirect(
                f"{self.admin_login_path}?next={request.get_full_path()}"
            )

        return self.get_response(request)
