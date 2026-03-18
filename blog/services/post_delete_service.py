import logging
from datetime import timedelta
from django.db import transaction
from blog.models import Post, PostImage

logger = logging.getLogger(__name__)


# 게시물 삭제 후 관련 이미지 post_id, updated_at 수정
def mark_post_images_for_cleanup(post: Post) -> None:
    post_images = PostImage.objects.filter(post=post)

    for post_image in post_images:
        post_image.post = None
        post_image.save(update_fields=["post", "updated_at"])


# 썸네일 삭제
def delete_post_preview_image(post: Post) -> None:
    if not post.preview_image or not post.preview_image.name:
        return

    file_name = post.preview_image.name
    storage = post.preview_image.storage
    path = post.preview_image.path

    try:
        storage.delete(file_name)
    except Exception:
        logger.exception(
            "Post preview image delete failed",
            extra={
                "post_id": post.id,
                "file_name": file_name,
                "path": path,
            },
        )


# 게시물 삭제
@transaction.atomic
def delete_post(post: Post) -> None:
    mark_post_images_for_cleanup(post)
    delete_post_preview_image(post)
    post.delete()
