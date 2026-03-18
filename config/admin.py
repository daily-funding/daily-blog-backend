from django.contrib.admin import AdminSite
from django.shortcuts import redirect


class CustomAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        return redirect("blog:admin-post-list")


custom_admin_site = CustomAdminSite(name="admin")
