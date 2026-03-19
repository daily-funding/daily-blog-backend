# cleanup command가 24시간 지난 orphan 이미지만 삭제하는지 테스트

from datetime import timedelta
from unittest.mock import patch

import boto3
import pytest
from django.core.management import call_command
from django.utils import timezone
from moto import mock_aws

from blog.models import PostImage


@pytest.fixture(autouse=True)
def aws_mock():
    with mock_aws():
        boto3.client("s3", region_name="ap-northeast-2").create_bucket(
            Bucket="dailyfunding-images",
            CreateBucketConfiguration={"LocationConstraint": "ap-northeast-2"},
        )
        yield


@pytest.mark.django_db
def test_cleanup_orphan_post_images_deletes_only_old_orphan_images(
    post,
    post_image_factory,
):
    old_orphan_image = post_image_factory(
        post=None,
        filename="old.png",
        capacity=10,
    )
    recent_orphan_image = post_image_factory(
        post=None,
        filename="recent.png",
        capacity=11,
    )
    attached_image = post_image_factory(
        post=post,
        filename="attached.png",
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
