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

@pytest.mark.django_db
class TestCategoryListView:

    def test_retrieve_categories(self):
        # given
        client = APIClient()
        category1 = create_category(name="카테고리1")
        category2 = create_category(name="카테고리2")

        # when
        response = client.get("/categories/")

        # then
        assert response.status_code == 200
        assert len(response.data["categories"]) == 2
        assert response.data["categories"][0]["category_id"] == category1.id
        assert response.data["categories"][0]["name"] == category1.name
        assert response.data["categories"][1]["category_id"] == category2.id
        assert response.data["categories"][1]["name"] == category2.name

    def test_return_empty_list_when_no_data(self):
        # given
        client = APIClient()

        # when
        response = client.get("/categories/")

        # then
        assert response.status_code == 200
        assert len(response.data["categories"]) == 0
