from rest_framework.test import APIClient

import pytest

from blog.tests.fixture.category_fixture import create_category

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
