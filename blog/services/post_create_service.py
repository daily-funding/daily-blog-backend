import logging
import re

from django.conf import settings
from django.db import transaction

from blog.models import Post, PostImage

logger = logging.getLogger(__name__)

# 이미지 추출을 위한 이미지 패턴 정규식
IMG_SRC_PATTERN = re.compile(
    r'<img[^>]+src\s*=\s*["\']([^"\']+)["\']',
    re.IGNORECASE,
)


# 이미지 경로 문자열 리스트 반환
def extract_post_image_paths_from_html(content: str) -> list[str]:
    if not content:
        return []

    image_paths = []
    root = settings.POST_IMAGE_UPLOAD_ROOT
    root_without_slash = root.rstrip("/")

    # src 값만 추출함
    for src in IMG_SRC_PATTERN.findall(content):
        if root in src:
            image_paths.append(src[src.index(root) :])
        elif root_without_slash in src:
            start = src.index(root_without_slash)
            image_paths.append(src[start:])

    return image_paths


# 본문 내 이미지와 PostImage를 연결
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


# 관리자 게시물 생성 서비스
@transaction.atomic
def create_post(*, validated_data, author):
    post = Post.objects.create(
        author=author,
        **validated_data,
    )

    bind_post_images_to_post(post)

    return post
