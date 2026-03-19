from django.urls import path
from blog.views.admin_post_views import (
    admin_post_create_view,
    admin_post_list_view,
    admin_post_detail_view,
    admin_post_delete_view,
    admin_post_edit_view,
    admin_pin_add_view,
    admin_pin_remove_view,
    admin_pin_reorder_view,
)
from blog.views.admin_category_views import (
    admin_category_manage_view,
    admin_category_create_view,
    admin_category_delete_view,
)
from blog.views.admin_image_upload_views import admin_image_upload_view

app_name = "blog"

urlpatterns = [
    path("", admin_post_list_view, name="admin-post-list"),
    path("posts/create/", admin_post_create_view, name="admin-post-create"),
    path("posts/<int:post_id>/", admin_post_detail_view, name="admin-post-detail"),
    path(
        "posts/<int:post_id>/delete/",
        admin_post_delete_view,
        name="admin-post-delete",
    ),
    path(
        "posts/<int:post_id>/edit/",
        admin_post_edit_view,
        name="admin-post-edit",
    ),
    path("pins/add/<int:post_id>/", admin_pin_add_view, name="admin-pin-add"),
    path("pins/remove/<int:post_id>/", admin_pin_remove_view, name="admin-pin-remove"),
    path("pins/reorder/", admin_pin_reorder_view, name="admin-pin-reorder"),
    path("categories/", admin_category_manage_view, name="admin-category-manage"),
    path(
        "categories/create/", admin_category_create_view, name="admin-category-create"
    ),
    path(
        "categories/<int:category_id>/delete/",
        admin_category_delete_view,
        name="admin-category-delete",
    ),
    path("images/upload/", admin_image_upload_view, name="admin-image-upload"),
]
