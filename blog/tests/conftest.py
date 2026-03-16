# 관리자 로직 공통 fixture
import io
import pytest

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from blog.models import Category


def make_test_image_file(
    filename="test.png",
    content_type="image/png",
    size=(100, 100),
    color=(255, 0, 0),
):
    file_obj = io.BytesIO()
    image = Image.new("RGB", size, color)
    image.save(file_obj, format="PNG")
    file_obj.seek(0)

    return SimpleUploadedFile(
        name=filename,
        content=file_obj.read(),
        content_type=content_type,
    )


@pytest.fixture
def staff_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="staffuser",
        password="testpass123",
        is_staff=True,
    )


@pytest.fixture
def normal_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="normaluser",
        password="testpass123",
        is_staff=False,
    )


@pytest.fixture
def category(db):
    return Category.objects.create(name="스타트업 이야기")


@pytest.fixture
def preview_image_file():
    return make_test_image_file(filename="preview.png")


@pytest.fixture
def content_image_file():
    return make_test_image_file(filename="content.png")
