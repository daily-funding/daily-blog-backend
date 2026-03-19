from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode


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
                query_string = urlencode({"next": request.get_full_path()})
                return redirect(f"{self.admin_login_path}?{query_string}")
            return self.get_response(request)

        if not request.user.is_staff:
            raise Http404("페이지를 찾을 수 없습니다.")

        return self.get_response(request)
