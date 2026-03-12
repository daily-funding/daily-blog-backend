import boto3
from django.core.files.uploadedfile import SimpleUploadedFile
from moto import mock_aws
from rest_framework.test import APIClient

import pytest
from django.contrib.auth import get_user_model

from blog.models import Post, Category, POST_IMAGE_UPLOAD_PATH


@pytest.fixture(autouse=True)
def aws_mock():
    with mock_aws():
        boto3.client("s3", region_name="ap-northeast-2").create_bucket(
            Bucket="dailyfunding-images",
            CreateBucketConfiguration={"LocationConstraint": "ap-northeast-2"},
        )
        yield


@pytest.mark.django_db
class TestPostView:

    def test_retrieve_post(self):
        # given
        client = APIClient()
        user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass",
        )
        category = Category.objects.create(name="foobar")
        preview_image = SimpleUploadedFile(
            name="test.jpg",
            content=b"fake image content",
            content_type="image/jpeg",
        )
        post = Post.objects.create(
            category=category,
            author=user,
            title="title",
            subtitle="subtitle",
            description="description",
            content="content",
            preview_image=preview_image,
        )

        # when
        response = client.get(f"/posts/{post.id}/")

        # then
        assert response.status_code == 200
        assert response.data["post_id"] == post.id
        assert response.data["category_name"] == "foobar"
        assert response.data["title"] == "title"
        assert response.data["subtitle"] == "subtitle"
        assert response.data["content"] == "content"
        assert POST_IMAGE_UPLOAD_PATH in response.data["preview_image"]
