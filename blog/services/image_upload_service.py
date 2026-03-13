from django.core.exceptions import ValidationError

ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpg",
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
}

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB


def validate_uploaded_image(uploaded_file):
    if uploaded_file.content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
        raise ValidationError("이미지 파일만 업로드할 수 있습니다.")

    if uploaded_file.size > MAX_IMAGE_SIZE:
        raise ValidationError("이미지 파일 크기는 5MB 이하여야 합니다.")
