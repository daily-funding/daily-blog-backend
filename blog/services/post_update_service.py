from django.db import transaction

from blog.models import Post, PostImage
from blog.services.post_create_service import extract_post_image_paths_from_html


@transaction.atomic
def update_post(*, post: Post, validated_data: dict) -> Post:
    # 수정 전 상태 저장
    old_content = post.content
    old_preview_image = post.preview_image
    old_image_paths = set(extract_post_image_paths_from_html(old_content))

    for field, value in validated_data.items():
        setattr(post, field, value)

    post.save()

    # 수정 후 본문 이미지 경로
    new_image_paths = set(extract_post_image_paths_from_html(post.content))

    removed_image_paths = old_image_paths - new_image_paths
    added_image_paths = new_image_paths - old_image_paths

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

    # 썸네일 변경 시 기존 파일 S3에서 삭제
    if old_preview_image and old_preview_image != post.preview_image:
        old_preview_image.delete(save=False)

    return post
