import pytest

from django.urls import reverse

from blog.models import Category


@pytest.mark.django_db
def test_admin_category_create_rejects_case_insensitive_duplicates(client, staff_user):
    client.login(username="staffuser", password="testpass123")
    Category.objects.create(name="스타트업 이야기")

    response = client.post(
        reverse("blog:admin-category-create"),
        data={"name": "스타트업 이야기"},
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    assert response.status_code == 400
    assert response.json()["message"] == "이미 존재하는 카테고리입니다."


@pytest.mark.django_db
def test_admin_category_create_rejects_case_variant_duplicates(client, staff_user):
    client.login(username="staffuser", password="testpass123")
    Category.objects.create(name="Finance")

    response = client.post(
        reverse("blog:admin-category-create"),
        data={"name": "finance"},
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    assert response.status_code == 400
    assert response.json()["message"] == "이미 존재하는 카테고리입니다."
