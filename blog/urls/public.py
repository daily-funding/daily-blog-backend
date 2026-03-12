from django.urls import path
from blog.views.post_view import PostView

app_name = "blog"

urlpatterns = [
    path("<int:post_id>/", PostView.as_view(), name="post-detail"),
]
