from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
<<<<<<< HEAD
    path("admin/blog/", include("blog.urls.admin_urls")), #admin보다 위에 와야함
=======
    path("blog/admin/", include("blog.urls.admin")),
>>>>>>> a849016 (blog/admin/ url 추가)
    path("admin/", admin.site.urls),
    path("posts/", include("blog.urls.public_urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
