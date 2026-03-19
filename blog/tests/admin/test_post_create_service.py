# 생성 로직 / 이미지 연결
import pytest

from blog.models import Post, PostImage
from blog.services.post_create_service import create_post
from blog.services.post_content_sanitize_service import sanitize_post_content

pytestmark = pytest.mark.usefixtures("aws_mock")


@pytest.mark.django_db
def test_create_post_binds_post_images_when_content_contains_image_paths(
    category,
    staff_user,
):
    post_image_1 = PostImage.objects.create(
        post=None,
        path="images/posts/a.png",
        capacity=100,
    )
    post_image_2 = PostImage.objects.create(
        post=None,
        path="images/posts/b.png",
        capacity=200,
    )

    validated_data = {
        "category": category,
        "title": "제목",
        "subtitle": "부제",
        "description": "설명",
        "content": """
            <p>본문</p>
            <img src="https://dailyfunding-images.s3.amazonaws.com/images/posts/a.png">
            <img src="https://dailyfunding-images.s3.amazonaws.com/images/posts/b.png">
        """,
        "preview_image": "images/posts/preview.png",
    }

    post = create_post(
        validated_data=validated_data,
        author=staff_user,
    )

    post_image_1.refresh_from_db()
    post_image_2.refresh_from_db()

    assert post_image_1.post == post
    assert post_image_2.post == post


@pytest.mark.django_db
def test_create_post_sets_author(category, staff_user):
    validated_data = {
        "category": category,
        "title": "제목",
        "subtitle": "부제",
        "description": "설명",
        "content": "<p>본문</p>",
        "preview_image": "images/posts/preview.png",
    }

    post = create_post(
        validated_data=validated_data,
        author=staff_user,
    )

    assert Post.objects.count() == 1
    assert post.author == staff_user


@pytest.mark.django_db
def test_create_post_keeps_unmatched_post_images_null(
    category,
    staff_user,
):
    post_image = PostImage.objects.create(
        post=None,
        path="images/posts/not-used.png",
        capacity=100,
    )

    validated_data = {
        "category": category,
        "title": "제목",
        "subtitle": "부제",
        "description": "설명",
        "content": "<p>본문에 이미지 없음</p>",
        "preview_image": "images/posts/preview.png",
    }

    create_post(
        validated_data=validated_data,
        author=staff_user,
    )

    post_image.refresh_from_db()

    assert post_image.post is None


@pytest.mark.django_db
def test_create_post_compresses_preview_image_to_webp(category, staff_user, preview_image_file):
    validated_data = {
        "category": category,
        "title": "제목",
        "subtitle": "부제",
        "description": "설명",
        "content": "<p>본문</p>",
        "preview_image": preview_image_file,
    }
    post = create_post(validated_data=validated_data, author=staff_user)

    assert post.preview_image.name.endswith(".webp")


# sanitize 검증
@pytest.mark.django_db
def test_post_content_sanitize_removes_script():
    raw = '<p>hello</p><script>alert("xss")</script>'

    sanitized = sanitize_post_content(raw)

    assert "<script>" not in sanitized
