import os
import uuid

from django.conf import settings
from django.db import models
from django.db.models import CASCADE, SET_NULL

POST_IMAGE_UPLOAD_PATH = "images/posts/"

def post_image_upload_to(instance, filename):  # s3의 images/posts/에 업로드 하는 함수
    ext = os.path.splitext(filename)[1].lower()
    return f"{POST_IMAGE_UPLOAD_PATH}/{uuid.uuid4()}{ext}"


class Category(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=SET_NULL, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    content = models.TextField()
    preview_image = models.ImageField(upload_to=post_image_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=SET_NULL, null=True)
    path = models.ImageField(upload_to=post_image_upload_to)
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Pin(models.Model):
    post = models.ForeignKey(Post, on_delete=CASCADE)
    sort_order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
