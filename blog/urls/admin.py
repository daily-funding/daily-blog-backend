from django.urls import path

from blog.views.admin_post_views import (
    admin_post_create_view,
    admin_post_list_view,
)

app_name = "blog"

urlpatterns = [
    path("posts/", admin_post_list_view, name="admin-post-list"),
    path("posts/create/", admin_post_create_view, name="admin-post-create"),
]
