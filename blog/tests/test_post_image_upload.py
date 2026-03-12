# 실제 modesl.py의 model 활용하여 s3에 업로드 하는 테스트 코드

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

    print("\n=== Post 생성 결과 확인 ===")
    print(f"Post ID: {post.id}")
    print(f"제목: {post.title}")
    print(f"작성자 ID: {post.author_id}")
    print(f"카테고리 ID: {post.category_id}")

    print("\n=== 이미지 필드 확인 ===")
    print(f"post.preview_image.name : {post.preview_image.name}")
    print(f"post.preview_image.url : {post.preview_image.url}")
    print(f"post.preview_image.size (byte단위): {post.preview_image.size}")
    print(f"post.preview_image.storage : {post.preview_image.storage}")
    print(f"파일 존재 여부(S3): {default_storage.exists(post.preview_image.name)}")

    print("\n=== 업로드 경로 형식 확인 ===")
    print(
        f"starts with 'images/posts/': {post.preview_image.name.startswith('images/posts/')}"
    )
    print(f"파일 확장자: {Path(post.preview_image.name).suffix}")

    assert post.preview_image.name.startswith("images/posts/")
    assert default_storage.exists(post.preview_image.name)
