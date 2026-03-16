# 접근 권한 / redirect / 상세보기

import pytest

from django.urls import reverse

from blog.models import Post, PostImage


@pytest.mark.django_db
def test_admin_post_create_view_requires_login(client):
    url = reverse("blog:admin-post-create")

    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_admin_post_create_view_denies_non_staff_user(client, normal_user):
    client.login(username="normaluser", password="testpass123")

    url = reverse("blog:admin-post-create")
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_admin_post_create_view_allows_staff_user(client, staff_user):
    client.login(username="staffuser", password="testpass123")

    url = reverse("blog:admin-post-create")
    response = client.get(url)

    assert response.status_code == 200
    assert "관리자 게시물 작성" in response.content.decode()


@pytest.mark.django_db
def test_admin_post_create_success_redirects_detail(
    client,
    staff_user,
    category,
    preview_image_file,
):
    client.login(username="staffuser", password="testpass123")

    url = reverse("blog:admin-post-create")
    response = client.post(
        url,
        data={
            "category": category.id,
            "title": "제목",
            "subtitle": "부제",
            "description": "설명",
            "content": "<p>본문</p>",
            "preview_image": preview_image_file,
        },
    )

    post = Post.objects.get()

    assert response.status_code == 302
    assert response.url == reverse(
        "blog:admin-post-detail", kwargs={"post_id": post.id}
    )
    assert post.author == staff_user


@pytest.mark.django_db
def test_admin_post_create_invalid_renders_form_again(
    client,
    staff_user,
    category,
    preview_image_file,
):
    client.login(username="staffuser", password="testpass123")

    url = reverse("blog:admin-post-create")
    response = client.post(
        url,
        data={
            "category": category.id,
            "title": "   ",
            "subtitle": "부제",
            "description": "설명",
            "content": "<p>본문</p>",
            "preview_image": preview_image_file,
        },
    )

    assert response.status_code == 200
    assert Post.objects.count() == 0


@pytest.mark.django_db
def test_admin_post_detail_view_renders_post(client, staff_user, category):
    client.login(username="staffuser", password="testpass123")

    post = Post.objects.create(
        category=category,
        author=staff_user,
        title="제목",
        subtitle="부제",
        description="설명",
        content="<p>본문</p>",
        preview_image="images/posts/preview.png",
    )

    url = reverse("blog:admin-post-detail", kwargs={"post_id": post.id})
    response = client.get(url)

    assert response.status_code == 200
    assert "제목" in response.content.decode()


@pytest.mark.django_db
def test_admin_post_create_connects_post_images(
    client,
    staff_user,
    category,
    preview_image_file,
):
    client.login(username="staffuser", password="testpass123")

    PostImage.objects.create(
        post=None,
        path="images/posts/a.png",
        capacity=100,
    )

    url = reverse("blog:admin-post-create")
    response = client.post(
        url,
        data={
            "category": category.id,
            "title": "제목",
            "subtitle": "부제",
            "description": "설명",
            "content": '<p>본문 <img src="https://dailyfunding-images.s3.amazonaws.com/images/posts/a.png"></p>',
            "preview_image": preview_image_file,
        },
    )

    post = Post.objects.get()
    linked_image = PostImage.objects.get(path="images/posts/a.png")

    assert response.status_code == 302
    assert linked_image.post == post
