from django.urls import path

from blog.views.category_views import category_list

urlpatterns = [
    path("", category_list)
]
