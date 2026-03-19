#  storage 삭제 실패 시 DB row 유지 테스트

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
def test_cleanup_orphan_post_images_keeps_db_row_when_storage_delete_fails(
    post_image_factory,
):
    post_image = post_image_factory(
        post=None,
        filename="fail.png",
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
