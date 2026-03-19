# 관리자 로직 공통 fixture
import io
import os
import boto3
import pytest

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from moto import mock_aws
from PIL import Image

from blog.models import Post, PostImage, Category


@pytest.fixture
def aws_mock():
    with mock_aws():
        boto3.client("s3", region_name="ap-northeast-2").create_bucket(
            Bucket="dailyfunding-images",
            CreateBucketConfiguration={"LocationConstraint": "ap-northeast-2"},
        )
        yield


# 테스트용 이미지 파일 생성
def make_test_image_file(
    filename="test.png",
    content_type="image/png",
    size=(100, 100),
    color=(255, 0, 0),
):
    ext = os.path.splitext(filename)[1].lower()

    format_map = {
        ".png": ("PNG", "image/png"),
        ".jpg": ("JPEG", "image/jpeg"),
        ".jpeg": ("JPEG", "image/jpeg"),
        ".webp": ("WEBP", "image/webp"),
        ".gif": ("GIF", "image/gif"),
    }

    if ext not in format_map:
        raise ValueError(f"지원하지 않는 이미지 확장자입니다: {ext}")

    image_format, expected_content_type = format_map[ext]

    if content_type != expected_content_type:
        raise ValueError(
            f"filename 확장자와 content_type이 일치하지 않습니다: "
            f"{filename} / {content_type}"
        )

    file_obj = io.BytesIO()
    image = Image.new("RGB", size, color)
    image.save(file_obj, format=image_format)
    file_obj.seek(0)

    return SimpleUploadedFile(
        name=filename,
        content=file_obj.read(),
        content_type=content_type,
    )


# 관리자 유저 생성
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


@pytest.fixture
def post(staff_user, category):
    return Post.objects.create(
        category=category,
        author=staff_user,
        title="제목",
        subtitle="부제목",
        description="설명",
        content="본문",
    )


@pytest.fixture
def post_image_factory(db):
    def create_post_image(
        *,
        post=None,
        filename="content.png",
        content_type="image/png",
        size=(100, 100),
        color=(255, 0, 0),
        capacity=10,
    ):
        image_file = make_test_image_file(
            filename=filename,
            content_type=content_type,
            size=size,
            color=color,
        )

        return PostImage.objects.create(
            post=post,
            path=image_file,
            capacity=capacity,
        )

    return create_post_image
