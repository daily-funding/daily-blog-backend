from django.urls import path

from blog.views.post_views import PostDetailView, PostListView

urlpatterns = [
    path("<int:post_id>/", PostDetailView.as_view()),
    path("", PostListView.as_view()),

]
