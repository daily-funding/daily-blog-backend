from django.urls import path
from blog.views.post_view import PostView


urlpatterns = [
    path("<int:post_id>/", PostView.as_view()),
]
