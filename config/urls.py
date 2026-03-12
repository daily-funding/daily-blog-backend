from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/blog/", include("blog.urls.admin")),
    path("admin/", admin.site.urls),
    path("posts/", include("blog.urls.public")),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
