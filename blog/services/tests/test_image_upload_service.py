from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

from blog.services.image_upload_service import compress_to_webp
from blog.tests.admin.conftest import make_test_image_file


def test_compress_png_to_webp():
    uploaded = make_test_image_file("photo.png", "image/png")
    result = compress_to_webp(uploaded)

    assert isinstance(result, InMemoryUploadedFile)
    assert result.name == "photo.webp"
    assert result.content_type == "image/webp"

    result.seek(0)
    image = Image.open(result)
    assert image.format == "WEBP"


def test_compress_jpeg_to_webp():
    uploaded = make_test_image_file("photo.jpg", "image/jpeg")
    result = compress_to_webp(uploaded)

    assert result.name == "photo.webp"
    assert result.content_type == "image/webp"

    result.seek(0)
    image = Image.open(result)
    assert image.format == "WEBP"


def test_gif_is_not_converted():
    uploaded = make_test_image_file("anim.gif", "image/gif")
    result = compress_to_webp(uploaded)

    assert result is uploaded
    assert result.content_type == "image/gif"


def test_compress_webp_to_webp():
    uploaded = make_test_image_file("photo.webp", "image/webp")
    result = compress_to_webp(uploaded)

    assert result.name == "photo.webp"
    assert result.content_type == "image/webp"
