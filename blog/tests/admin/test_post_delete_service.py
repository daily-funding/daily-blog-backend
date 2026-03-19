# 게시물 삭제 시 PostImage.post = null / updated_at 갱신 테스트
from datetime import timedelta
from unittest.mock import Mock

import pytest
from django.utils import timezone

from blog.models import PostImage
from blog.services.post_delete_service import delete_post, delete_post_preview_image

pytestmark = pytest.mark.usefixtures("aws_mock")


@pytest.mark.django_db
def test_delete_post_marks_post_images_for_cleanup(post, post_image_factory):
    post_image = post_image_factory(
        post=post,
        filename="test.png",
        capacity=12,
    )

    old_updated_at = timezone.now() - timedelta(days=2)
    PostImage.objects.filter(id=post_image.id).update(updated_at=old_updated_at)
    post_image.refresh_from_db()

    delete_post(post)

    post_image.refresh_from_db()

    assert post_image.post is None
    assert post_image.updated_at > old_updated_at


@pytest.mark.django_db
def test_delete_post_preview_image_uses_storage_delete_without_path_access(
    post, preview_image_file
):
    post.preview_image = preview_image_file
    post.preview_image.name = "images/posts/preview.png"
    post.preview_image.storage.delete = Mock()

    delete_post_preview_image(post)

    post.preview_image.storage.delete.assert_called_once_with(
        "images/posts/preview.png"
    )
