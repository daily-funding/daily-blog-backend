#  storage 삭제 실패 시 DB row 유지 테스트

from datetime import timedelta
from unittest.mock import patch

import pytest
from django.core.management import call_command
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from blog.models import PostImage


@pytest.mark.django_db
def test_cleanup_orphan_post_images_keeps_db_row_when_storage_delete_fails():
    post_image = PostImage.objects.create(
        post=None,
        path=SimpleUploadedFile("fail.png", b"fail-file", content_type="image/png"),
        capacity=15,
    )

    old_time = timezone.now() - timedelta(hours=25)
    PostImage.objects.filter(id=post_image.id).update(updated_at=old_time)
    post_image.refresh_from_db()

    with patch.object(
        post_image.path.storage,
        "delete",
        side_effect=Exception("s3 delete failed"),
    ):
        call_command("cleanup_orphan_post_images")

    assert PostImage.objects.filter(id=post_image.id).exists()
