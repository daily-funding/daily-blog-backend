# 입력 검증

import pytest

from blog.forms.post_form import PostCreateForm


@pytest.mark.django_db
def test_post_create_form_valid(category, preview_image_file):
    form = PostCreateForm(
        data={
            "category": category.id,
            "title": "제목입니다",
            "subtitle": "부제목입니다",
            "description": "미리보기 설명입니다",
            "content": "<p>본문입니다</p>",
        },
        files={
            "preview_image": preview_image_file,
        },
    )

    assert form.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "field,value,error_message",
    [
        ("title", "   ", "제목은 비워둘 수 없습니다."),
        ("subtitle", "   ", "부제목은 비워둘 수 없습니다."),
        ("description", "   ", "미리보기 설명은 비워둘 수 없습니다."),
        ("content", "   ", "본문은 비워둘 수 없습니다."),
    ],
)
def test_post_create_form_blank_field_invalid(
    category,
    preview_image_file,
    field,
    value,
    error_message,
):
    data = {
        "category": category.id,
        "title": "제목입니다",
        "subtitle": "부제목입니다",
        "description": "미리보기 설명입니다",
        "content": "<p>본문입니다</p>",
    }
    data[field] = value

    form = PostCreateForm(
        data=data,
        files={"preview_image": preview_image_file},
    )

    assert not form.is_valid()
    assert field in form.errors
    assert form.errors[field] == [error_message]


@pytest.mark.django_db
def test_post_create_form_requires_preview_image(category):
    form = PostCreateForm(
        data={
            "category": category.id,
            "title": "제목입니다",
            "subtitle": "부제목입니다",
            "description": "미리보기 설명입니다",
            "content": "<p>본문입니다</p>",
        }
    )

    assert not form.is_valid()
    assert "preview_image" in form.errors
