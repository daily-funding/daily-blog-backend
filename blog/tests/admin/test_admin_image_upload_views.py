# 업로드 API / 파일 검증

import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from blog.models import PostImage

pytestmark = pytest.mark.usefixtures("aws_mock")


@pytest.mark.django_db
def test_admin_image_upload_success(client, staff_user, content_image_file):
    client.login(username="staffuser", password="testpass123")

    url = reverse("blog:admin-image-upload")
    response = client.post(
        url,
        data={"upload": content_image_file},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["uploaded"] == 1
    assert "url" in data
    assert PostImage.objects.filter(post__isnull=True).count() == 1
    assert data["fileName"].endswith(".webp")


@pytest.mark.django_db
@pytest.mark.parametrize("method_name", ["get", "put", "patch", "delete"])
def test_admin_image_upload_rejects_non_post_methods(
    client,
    staff_user,
    method_name,
):
    client.login(username="staffuser", password="testpass123")

    url = reverse("blog:admin-image-upload")
    response = getattr(client, method_name)(url)

    assert response.status_code == 400
    assert "POST 요청만 허용됩니다." in response.content.decode()


@pytest.mark.django_db
def test_admin_image_upload_rejects_missing_file(client, staff_user):
    client.login(username="staffuser", password="testpass123")

    url = reverse("blog:admin-image-upload")
    response = client.post(url, data={})

    assert response.status_code == 400
    data = response.json()
    assert data["uploaded"] == 0
    assert data["error"]["message"] == "업로드된 파일이 없습니다."


@pytest.mark.django_db
def test_admin_image_upload_rejects_invalid_content_type(client, staff_user):
    client.login(username="staffuser", password="testpass123")

    invalid_file = SimpleUploadedFile(
        "test.txt",
        b"not image",
        content_type="text/plain",
    )

    url = reverse("blog:admin-image-upload")
    response = client.post(
        url,
        data={"upload": invalid_file},
    )

    assert response.status_code == 400
    data = response.json()
    assert data["uploaded"] == 0
    assert "지원하지 않는 이미지 형식입니다." in data["error"]["message"]


@pytest.mark.django_db
def test_admin_image_upload_rejects_corrupted_image_file(client, staff_user):
    client.login(username="staffuser", password="testpass123")

    invalid_image = SimpleUploadedFile(
        "fake.png",
        b"not really image bytes",
        content_type="image/png",
    )

    url = reverse("blog:admin-image-upload")
    response = client.post(
        url,
        data={"upload": invalid_image},
    )

    assert response.status_code == 400
    data = response.json()
    assert data["uploaded"] == 0
    assert data["error"]["message"] == "유효한 이미지 파일이 아닙니다."


@pytest.mark.django_db
def test_post_image_delete():
    image = PostImage.objects.create(
        post=None,
        path="images/posts/test.png",
        capacity=100,
    )

    image_id = image.id

    image.delete()

    assert not PostImage.objects.filter(id=image_id).exists()
