# 실제 modesl.py의 upload 함수 이용하여 s3에 업로드 하는 테스트 코드

import pytest
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.storage import default_storage

from blog.models import Post, Category


@pytest.mark.django_db
def test_post_image_upload():
    User = get_user_model()

    user = User.objects.create_user(
        username="testuser",
        password="testpass",
    )

    category = Category.objects.create(name="test")

    image_path = Path("images/test.jpg")

    with open(image_path, "rb") as img:
        post = Post.objects.create(
            category=category,
            author=user,
            title="pytest title",
            subtitle="pytest subtitle",
            description="pytest description",
            content="pytest content",
            preview_image=File(img, name=image_path.name),
        )

    assert post.preview_image.name.startswith("images/posts")
    assert default_storage.exists(post.preview_image.name)
