from django.contrib import admin
from django.urls import path, include, reverse
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from config.admin import custom_admin_site


def root_redirect_to_admin_login(request):
    login_url = reverse("admin:login")
    next_url = reverse("blog:admin-post-list")
    return redirect(f"{login_url}?next={next_url}")


urlpatterns = [
    path("", root_redirect_to_admin_login),
    path("admin/blog/", include("blog.urls.admin_urls")),  # admin보다 위에 와야함
    path("admin/", custom_admin_site.urls),
    path("posts/", include("blog.urls.post_urls")),
    path("categories/", include("blog.urls.category_urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),  # ckeditor 경로
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
