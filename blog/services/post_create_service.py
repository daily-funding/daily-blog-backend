from django.db import transaction

from blog.models import Post
from blog.services.post_image_service import (
    bind_post_images_to_post,
    compress_preview_image_if_uploaded,
)


@transaction.atomic
def create_post(*, validated_data, author):
    validated_data = compress_preview_image_if_uploaded(validated_data)

    post = Post.objects.create(
        author=author,
        **validated_data,
    )

    bind_post_images_to_post(post)

    return post
