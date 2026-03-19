import io
import os

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageOps, UnidentifiedImageError

ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
}

MAX_IMAGE_SIZE = 20 * 1024 * 1024  # 20MB


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


def compress_to_webp(uploaded_file) -> InMemoryUploadedFile:
    """
    JPEG/PNG/WebP 이미지를 WebP quality=75로 압축하여 반환.
    GIF는 변환하지 않고 원본 반환.
    """
    if uploaded_file.content_type == "image/gif":
        return uploaded_file

    uploaded_file.seek(0)  # 파일 포인터 초기화
    image = Image.open(uploaded_file)  # 이미지 메모리 로드

    image = ImageOps.exif_transpose(image)  # EXIF 회전 보정

    output = io.BytesIO()  # 메모리 버퍼에 작성
    image.save(output, format="WEBP", quality=75)  # webp/q:75로 압축
    output.seek(0)  # 파일 포인터 초기화

    original_name = os.path.splitext(uploaded_file.name)[0]
    new_name = f"{original_name}.webp"

    return InMemoryUploadedFile(
        file=output,
        field_name=None,
        name=new_name,
        content_type="image/webp",
        size=output.getbuffer().nbytes,
        charset=None,
    )
