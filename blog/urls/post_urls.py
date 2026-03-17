from django.urls import path
from blog.views.post_views import (
    post_list,
    top_post_list,
    post_detail,
    insight_post_list,
)

urlpatterns = [
    path("<int:post_id>/insight/", insight_post_list),
    path("<int:post_id>/", post_detail),
    path("top/", top_post_list),
    path("", post_list),
]
