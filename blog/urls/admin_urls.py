from django.urls import path
from blog.views.admin_post_views import (
    admin_post_create_view,
    admin_post_list_view,
    admin_post_detail_view,
    admin_post_delete_view,
)
from blog.views.admin_image_upload_views import admin_image_upload_view

app_name = "blog"

urlpatterns = [
    path("posts/", admin_post_list_view, name="admin-post-list"),
    path(
        "posts/create/",
        admin_post_create_view,
        name="admin-post-create",
    ),
    path(
        "posts/<int:post_id>/",
        admin_post_detail_view,
        name="admin-post-detail",
    ),
    path(
        "posts/<int:post_id>/delete/",
        admin_post_delete_view,
        name="admin-post-delete",
    ),
    path("images/upload/", admin_image_upload_view, name="admin-image-upload"),
]
