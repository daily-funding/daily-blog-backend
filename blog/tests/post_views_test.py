import boto3
from django.core.files.uploadedfile import SimpleUploadedFile
from moto import mock_aws
from rest_framework.test import APIClient

import pytest

from blog.models import POST_IMAGE_UPLOAD_PATH
from blog.tests.fixture.category_fixture import create_category
from blog.tests.fixture.pin_fixture import create_pin
from blog.tests.fixture.post_fixture import create_post
from blog.tests.fixture.user_fixture import create_user

from freezegun import freeze_time


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
        assert response.data["category_id"] == category.id
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
        response = client.get(f"/posts/?page=1&category_id={category1.id}")

        # then
        assert response.status_code == 200
        assert response.data["count"] == 5
        assert response.data["next"] is None
        assert response.data["previous"] is None
        assert len(response.data["results"]) == 5
        assert all(
            post["category_name"] == category1.name for post in response.data["results"]
        )

    def test_retrieve_posts_order_by_created_at_desc(self):
        # given
        client = APIClient()
        user = create_user()
        category = create_category()
        preview_image = SimpleUploadedFile(
            name="test.jpg",
            content=b"fake image content",
            content_type="image/jpeg",
        )
        with freeze_time("2024-01-02 00:00:00"):
            post1 = create_post(category=category, preview_image=preview_image, author=user)

        with freeze_time("2024-01-03 00:00:00"):
            post2 = create_post(category=category, preview_image=preview_image, author=user)

        with freeze_time("2024-01-01 00:00:00"):
            post3 = create_post(category=category, preview_image=preview_image, author=user)

        # when
        response = client.get("/posts/")

        # then
        assert response.status_code == 200
        assert response.data["results"][0]["post_id"] == post2.id
        assert response.data["results"][1]["post_id"] == post1.id
        assert response.data["results"][2]["post_id"] == post3.id


@pytest.mark.django_db
class TestTopPostListView:

    def test_retrieve_top_posts(self):
        # given
        client = APIClient()
        user = create_user()
        category = create_category()
        preview_image = SimpleUploadedFile(
            name="test.jpg",
            content=b"fake image content",
            content_type="image/jpeg",
        )
        post1 = create_post(category=category, preview_image=preview_image, author=user)
        post2 = create_post(category=category, preview_image=preview_image, author=user)

        create_pin(post=post1, sort_order=1)

        # when
        response = client.get("/posts/top/")

        # then
        assert response.status_code == 200
        assert len(response.data["posts"]) == 1
        assert response.data["posts"][0]["post_id"] == post1.id
        assert response.data["posts"][0]["category_id"] == category.id
        assert response.data["posts"][0]["category_name"] == category.name
        assert response.data["posts"][0]["title"] == post1.title
        assert response.data["posts"][0]["subtitle"] == post1.subtitle
        assert POST_IMAGE_UPLOAD_PATH in response.data["posts"][0]["preview_image"]

    def test_retrieve_top_posts_order_by_sort_order(self):
        # given
        client = APIClient()
        user = create_user()
        category = create_category()
        preview_image = SimpleUploadedFile(
            name="test.jpg",
            content=b"fake image content",
            content_type="image/jpeg",
        )
        post1 = create_post(category=category, preview_image=preview_image, author=user)
        post2 = create_post(category=category, preview_image=preview_image, author=user)
        post3 = create_post(category=category, preview_image=preview_image, author=user)
        post4 = create_post(category=category, preview_image=preview_image, author=user)

        create_pin(post=post1, sort_order=1)
        create_pin(post=post3, sort_order=2)
        create_pin(post=post4, sort_order=3)
        create_pin(post=post2, sort_order=4)

        # when
        response = client.get("/posts/top/")

        # then
        assert response.status_code == 200
        assert response.data["posts"][0]["post_id"] == post1.id
        assert response.data["posts"][1]["post_id"] == post3.id
        assert response.data["posts"][2]["post_id"] == post4.id
        assert response.data["posts"][3]["post_id"] == post2.id

@pytest.mark.django_db
class TestInsightPostListView:

    def test_retrieve_insight_posts(self):
        # given
        client = APIClient()
        user = create_user()
        category1 = create_category()
        category2 = create_category()
        preview_image = SimpleUploadedFile(
            name="test.jpg",
            content=b"fake image content",
            content_type="image/jpeg",
        )
        with freeze_time("2024-01-01 00:00:00"):
            post1 = create_post(category=category1, preview_image=preview_image, author=user)
        with freeze_time("2024-01-02 00:00:00"):
            post2 = create_post(category=category1, preview_image=preview_image, author=user)
        with freeze_time("2024-01-03 00:00:00"):
            post3 = create_post(category=category1, preview_image=preview_image, author=user)
        with freeze_time("2024-01-04 00:00:00"):
            post4 = create_post(category=category2, preview_image=preview_image, author=user)
        with freeze_time("2024-01-05 00:00:00"):
            post5 = create_post(category=category1, preview_image=preview_image, author=user)
        with freeze_time("2024-01-06 00:00:00"):
            post6 = create_post(category=category1, preview_image=preview_image, author=user)
        with freeze_time("2024-01-07 00:00:00"):
            post7 = create_post(category=category1, preview_image=preview_image, author=user)
        with freeze_time("2024-01-08 00:00:00"):
            post8 = create_post(category=category1, preview_image=preview_image, author=user)
        with freeze_time("2024-01-09 00:00:00"):
            post9 = create_post(category=category1, preview_image=preview_image, author=user)

        # when
        response = client.get(f"/posts/{post3.id}/insight/")

        # then
        """
        다른 카테고리인 post4, 본 게시물인 post3은 필터링된다.
        post1는 최신순 6개에 들지 않아 제외된다.
        """
        assert response.status_code == 200
        assert len(response.data["posts"]) == 6
        assert response.data["posts"][0]["post_id"] == post9.id
        assert response.data["posts"][1]["post_id"] == post8.id
        assert response.data["posts"][2]["post_id"] == post7.id
        assert response.data["posts"][3]["post_id"] == post6.id
        assert response.data["posts"][4]["post_id"] == post5.id
        assert response.data["posts"][5]["post_id"] == post2.id
        assert (post["post_id"] != post4.id for post in response.data["posts"])
