from django.db import transaction

from blog.models import Post
from blog.services.post_image_service import (
    compress_preview_image_if_uploaded,
    sync_embedded_post_images,
)


@transaction.atomic
def update_post(*, post: Post, validated_data: dict) -> Post:
    old_content = post.content
    old_preview_image_name = post.preview_image.name if post.preview_image else None

    validated_data = compress_preview_image_if_uploaded(validated_data)

    for field, value in validated_data.items():
        setattr(post, field, value)

    post.save()

    sync_embedded_post_images(
        post=post,
        old_content=old_content,
        new_content=post.content,
    )

    new_preview_image_name = post.preview_image.name if post.preview_image else None
    if old_preview_image_name and old_preview_image_name != new_preview_image_name:
        post.preview_image.storage.delete(old_preview_image_name)

    return post
