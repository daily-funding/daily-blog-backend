# 게시물 삭제 시 PostImage.post = null / updated_at 갱신 테스트
from datetime import timedelta

import boto3
import pytest
from django.utils import timezone
from moto import mock_aws

from blog.models import PostImage
from blog.services.post_delete_service import delete_post


@pytest.fixture(autouse=True)
def aws_mock():
    with mock_aws():
        boto3.client("s3", region_name="ap-northeast-2").create_bucket(
            Bucket="dailyfunding-images",
            CreateBucketConfiguration={"LocationConstraint": "ap-northeast-2"},
        )
        yield


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
