from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from blog.views.admin_post_views import (
    admin_post_create_view,
    admin_post_list_view,
)

app_name = "blog"

urlpatterns = [
    path("posts/", staff_member_required(admin_post_list_view), name="admin-post-list"),
    path(
        "posts/create/",
        staff_member_required(admin_post_create_view),
        name="admin-post-create",
    ),
]
