import logging
import re

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from blog.models import Post, PostImage
from blog.services.image_upload_service import compress_to_webp

logger = logging.getLogger(__name__)

IMG_SRC_PATTERN = re.compile(
    r'<img[^>]+src\s*=\s*["\']([^"\']+)["\']',
    re.IGNORECASE,
)


def extract_post_image_paths_from_html(content: str) -> list[str]:
    if not content:
        return []

    image_paths = []
    root = settings.POST_IMAGE_UPLOAD_ROOT
    root_without_slash = root.rstrip("/")

    for src in IMG_SRC_PATTERN.findall(content):
        if root in src:
            image_paths.append(src[src.index(root) :])
        elif root_without_slash in src:
            start = src.index(root_without_slash)
            image_paths.append(src[start:])

    return image_paths


def compress_preview_image_if_uploaded(validated_data: dict) -> dict:
    preview_image = validated_data.get("preview_image")

    if isinstance(preview_image, UploadedFile):
        validated_data["preview_image"] = compress_to_webp(preview_image)

    return validated_data


def bind_post_images_to_post(post: Post) -> None:
    image_paths = extract_post_image_paths_from_html(post.content)

    if not image_paths:
        return

    unique_image_paths = list(dict.fromkeys(image_paths))

    updated_count = PostImage.objects.filter(
        post__isnull=True,
        path__in=unique_image_paths,
    ).update(post=post)

    if updated_count != len(unique_image_paths):
        logger.warning(
            "일부 추출된 이미지가 매핑에 실패했습니다.",
            extra={
                "post_id": post.id,
                "extracted_count": len(image_paths),
                "unique_extracted_count": len(unique_image_paths),
                "updated_count": updated_count,
                "image_paths": image_paths,
                "unique_image_paths": unique_image_paths,
            },
        )


def sync_embedded_post_images(
    *, post: Post, old_content: str, new_content: str
) -> None:
    old_image_paths = set(extract_post_image_paths_from_html(old_content))
    new_image_paths = set(extract_post_image_paths_from_html(new_content))

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
