from django.urls import path
<<<<<<< HEAD
from blog.views.post_views import PostDetailView, PostListView

urlpatterns = [
    path("<int:post_id>/", PostDetailView.as_view()),
    path("", PostListView.as_view()),
=======
from blog.views.post_view import PostView


urlpatterns = [
    path("<int:post_id>/", PostView.as_view()),
>>>>>>> 2790c28 (chore: url 파일명 수정)
]
