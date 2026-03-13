import boto3
from django.core.files.uploadedfile import SimpleUploadedFile
from moto import mock_aws
from rest_framework.test import APIClient

import pytest

from blog.models import POST_IMAGE_UPLOAD_PATH
from blog.tests.fixture.category_fixture import create_category
from blog.tests.fixture.post_fixture import create_post
from blog.tests.fixture.user_fixture import create_user


@pytest.fixture(autouse=True)
def aws_mock():
    with mock_aws():
        boto3.client("s3", region_name="ap-northeast-2").create_bucket(
            Bucket="dailyfunding-images",
            CreateBucketConfiguration={"LocationConstraint": "ap-northeast-2"},
        )
        yield


@pytest.mark.django_db
class TestPostDetailView:

    def test_retrieve_post(self):
        # given
        client = APIClient()
        user = create_user()
        category = create_category()
        preview_image = SimpleUploadedFile(
            name="test.jpg",
            content=b"fake image content",
            content_type="image/jpeg",
        )
        post = create_post(category=category, preview_image=preview_image, author=user)

        # when
        response = client.get(f"/posts/{post.id}/")

        # then
        assert response.status_code == 200
        assert response.data["post_id"] == post.id
        assert response.data["category_name"] == category.name
        assert response.data["title"] == post.title
        assert response.data["subtitle"] == post.subtitle
        assert response.data["content"] == post.content
        assert POST_IMAGE_UPLOAD_PATH in response.data["preview_image"]


@pytest.mark.django_db
class TestPostListView:

    def test_retrieve_posts(self):
        # given
        client = APIClient()
        user = create_user()
        category1 = create_category(name="카테고리1")
        category2 = create_category(name="카테고리2")
        preview_image = SimpleUploadedFile(
            name="test.jpg",
            content=b"fake image content",
            content_type="image/jpeg",
        )
        for _ in range(5):
            create_post(category=category1, preview_image=preview_image, author=user)

        for _ in range(5):
            create_post(category=category2, preview_image=preview_image, author=user)

        # when
        response = client.get("/posts/")
        print(response.data)

        # then
        assert response.status_code == 200
        assert response.data["count"] == 10
        assert response.data["next"] is not None
        assert response.data["previous"] is None
        assert len(response.data["results"]) == 6

    def test_retrieve_last_page_posts(self):
        # given
        client = APIClient()
        user = create_user()
        category1 = create_category(name="카테고리1")
        category2 = create_category(name="카테고리2")
        preview_image = SimpleUploadedFile(
            name="test.jpg",
            content=b"fake image content",
            content_type="image/jpeg",
        )
        for _ in range(5):
            create_post(category=category1, preview_image=preview_image, author=user)

        for _ in range(5):
            create_post(category=category2, preview_image=preview_image, author=user)

        # when
        response = client.get("/posts/?page=2")

        # then
        assert response.status_code == 200
        assert response.data["count"] == 10
        assert response.data["next"] is None
        assert response.data["previous"] is not None
        assert len(response.data["results"]) == 4

    def test_return_empty_list_when_no_data(self):
        # given
        client = APIClient()

        # when
        response = client.get("/posts/")

        # then
        assert response.status_code == 200
        assert response.data["count"] == 0
        assert response.data["next"] is None
        assert response.data["previous"] is None
        assert len(response.data["results"]) == 0

    def test_return_404_when_invalid_page(self):
        # given
        client = APIClient()
        user = create_user()
        category = create_category()
        preview_image = SimpleUploadedFile(
            name="test.jpg",
            content=b"fake image content",
            content_type="image/jpeg",
        )
        create_post(category=category, preview_image=preview_image, author=user)

        # when
        response = client.get("/posts/?page=3")

        # then
        assert response.status_code == 404

    def test_retrieve_posts_by_category(self):
        # given
        client = APIClient()
        user = create_user()
        category1 = create_category(name="카테고리1")
        category2 = create_category(name="카테고리2")
        preview_image = SimpleUploadedFile(
            name="test.jpg",
            content=b"fake image content",
            content_type="image/jpeg",
        )
        for _ in range(5):
            create_post(category=category1, preview_image=preview_image, author=user)

        for _ in range(5):
            create_post(category=category2, preview_image=preview_image, author=user)

        # when
        response = client.get("/posts/?page=1&category_id=1")

        # then
        assert response.status_code == 200
        assert response.data["count"] == 5
        assert response.data["next"] is None
        assert response.data["previous"] is None
        assert len(response.data["results"]) == 5
