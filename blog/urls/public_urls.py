from django.urls import path
from blog.views.post_views import PostDetailView, PostListView, TopPostListView

urlpatterns = [
    path("<int:post_id>/", PostDetailView.as_view()),
    path("top/", TopPostListView.as_view()),
    path("", PostListView.as_view()),
]
