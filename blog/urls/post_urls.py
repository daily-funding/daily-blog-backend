from django.urls import path
from blog.views.post_views import (
    post_list,
    top_post_list,
    post_detail,
)

urlpatterns = [
    path("<int:post_id>/", post_detail),
    path("top/", top_post_list),
    path("", post_list),
]
