from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError

ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
}

MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_uploaded_image(uploaded_file):
    if not uploaded_file:
        raise ValidationError("이미지 파일이 필요합니다.")

    if uploaded_file.content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
        raise ValidationError(
            "지원하지 않는 이미지 형식입니다. " "지원 형식: JPEG, PNG, GIF, WEBP"
        )

    if uploaded_file.size > MAX_IMAGE_SIZE:
        max_size_mb = MAX_IMAGE_SIZE // (1024 * 1024)
        raise ValidationError(f"이미지 파일 크기는 {max_size_mb}MB 이하여야 합니다.")

    try:
        uploaded_file.seek(0)
        image = Image.open(uploaded_file)
        image.verify()
        uploaded_file.seek(0)
    except (UnidentifiedImageError, OSError):
        # 실제 파일이 진짜 이미지인지 확인
        raise ValidationError("유효한 이미지 파일이 아닙니다.")
