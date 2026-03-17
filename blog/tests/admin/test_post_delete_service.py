# 게시물 삭제 시 PostImage.post = null / updated_at 갱신 테스트
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from blog.models import Category, Post, PostImage
from blog.services.post_delete_service import delete_post


User = get_user_model()


@pytest.mark.django_db
def test_delete_post_marks_post_images_for_cleanup():
    user = User.objects.create_user(
        username="staffuser",
        password="testpass123",
        is_staff=True,
    )
    category = Category.objects.create(name="테스트 카테고리")

    post = Post.objects.create(
        category=category,
        author=user,
        title="제목",
        subtitle="부제목",
        description="설명",
        content="본문",
    )

    post_image = PostImage.objects.create(
        post=post,
        path=SimpleUploadedFile("test.png", b"file-content", content_type="image/png"),
        capacity=12,
    )

    old_updated_at = timezone.now() - timedelta(days=2)
    PostImage.objects.filter(id=post_image.id).update(updated_at=old_updated_at)
    post_image.refresh_from_db()

    delete_post(post)

    post_image.refresh_from_db()

    assert post_image.post is None
    assert post_image.updated_at > old_updated_at
