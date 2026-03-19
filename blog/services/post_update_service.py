from django.db import transaction

from blog.models import Post, PostImage
from blog.services.post_create_service import extract_post_image_paths_from_html


@transaction.atomic
def update_post(*, post: Post, validated_data: dict) -> Post:
    # 수정 전 본문 (이미지 비교용)
    old_content = post.content
    # 기존 본문에 포함된 이미지 경로 추출
    old_image_paths = set(extract_post_image_paths_from_html(old_content))

    for field, value in validated_data.items():
        setattr(post, field, value)

    # DB 저장
    post.save()

    # 수정 후 본문에서 이미지 경로 다시 추출
    new_image_paths = set(extract_post_image_paths_from_html(post.content))

    # 삭제된 이미지 / 새로 추가된 이미지 계산
    removed_image_paths = old_image_paths - new_image_paths
    added_image_paths = new_image_paths - old_image_paths

    # 본문에서 제거된 이미지를 post 연결 해제, 새로 추가된 이미지 현재 post에 연결
    if removed_image_paths:
        PostImage.objects.filter(
            post=post,
            path__in=removed_image_paths,
        ).update(post=None)

    if added_image_paths:
        PostImage.objects.filter(
            post__isnull=True,
            path__in=added_image_paths,
        ).update(post=post)

    return post
