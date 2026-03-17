# cleanup command가 24시간 지난 orphan 이미지만 삭제하는지 테스트

from datetime import timedelta
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from blog.models import Category, Post, PostImage


User = get_user_model()


@pytest.mark.django_db
def test_cleanup_orphan_post_images_deletes_only_old_orphan_images():
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

    old_orphan_image = PostImage.objects.create(
        post=None,
        path=SimpleUploadedFile("old.png", b"old-file", content_type="image/png"),
        capacity=10,
    )
    recent_orphan_image = PostImage.objects.create(
        post=None,
        path=SimpleUploadedFile("recent.png", b"recent-file", content_type="image/png"),
        capacity=11,
    )
    attached_image = PostImage.objects.create(
        post=post,
        path=SimpleUploadedFile(
            "attached.png", b"attached-file", content_type="image/png"
        ),
        capacity=12,
    )

    cutoff_old = timezone.now() - timedelta(hours=25)
    cutoff_recent = timezone.now() - timedelta(hours=23)

    PostImage.objects.filter(id=old_orphan_image.id).update(updated_at=cutoff_old)
    PostImage.objects.filter(id=recent_orphan_image.id).update(updated_at=cutoff_recent)
    PostImage.objects.filter(id=attached_image.id).update(updated_at=cutoff_old)

    old_orphan_image.refresh_from_db()
    recent_orphan_image.refresh_from_db()
    attached_image.refresh_from_db()

    with patch.object(old_orphan_image.path.storage, "delete") as mocked_delete:
        call_command("cleanup_orphan_post_images")

        mocked_delete.assert_called_once_with(old_orphan_image.path.name)

    assert not PostImage.objects.filter(id=old_orphan_image.id).exists()
    assert PostImage.objects.filter(id=recent_orphan_image.id).exists()
    assert PostImage.objects.filter(id=attached_image.id).exists()
